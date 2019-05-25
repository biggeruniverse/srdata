#util.py
import sys
import stackless
import contextlib
import weakref
import collections
from . import main
from .errors import TimeoutError, CancelledError
from .base import atomic, time
from . import app

WaitTimeoutError = TimeoutError # backwards compatibility

class local(object):
    """Tasklet local storage.  Similar to threading.local"""
    def __init__(self):
        object.__getattribute__(self, "__dict__")["_tasklets"] = weakref.WeakKeyDictionary()

    def get_dict(self):
        d = object.__getattribute__(self, "__dict__")["_tasklets"]
        try:
            a = d[stackless.getcurrent()]
        except KeyError:
            a = {}
            d[stackless.getcurrent()] = a
        return a

    def __getattribute__(self, name):
        a = object.__getattribute__(self, "get_dict")()
        if name == "__dict__":
            return a
        elif name in a:
            return a[name]
        else:
            return object.__getattribute__(self, name)


    def __setattr__(self, name, value):
        a = object.__getattribute__(self, "get_dict")()
        a[name] = value

    def __delattr__(self, name):
        a = object.__getattribute__(self, "get_dict")()
        try:
            del a[name]
        except KeyError:
            raise AttributeError(name)


def channel_wait(chan, timeout=None, exc=None):
    """channel.receive with an optional timeout"""
    with _timeout(timeout, blocked=True, exc=exc):
        return chan.receive()

def send_throw(channel, exc, val=None, tb=None):
    """send exceptions over a channel.  Has the same semantics
       for exc, val and tb as the raise statement has.  Use this
       for backwards compatibility with versions of stackless that
       don't have the "send_throw" method on channels.
    """
    if hasattr(channel, "send_throw"):
        return channel.send_throw(exc, val, tb)
    #currently, channel.send_exception allows only (type, arg1, ...)
    #and can"t cope with tb
    if exc is None:
        if val is None:
            val = sys.exc_info()[1]
        exc = val.__class__
    elif val is None:
        if isinstance(type, exc):
            exc, val = exc, ()
        else:
            exc, val = exc.__class__, exc
    if not isinstance(val, tuple):
        val = val.args
    channel.send_exception(exc, *val)

def tasklet_throw(tasklet, exc, val=None, tb=None, pending=False):
    """
    Throw an exception on a tasklet.  Emulates the new functionality
    for those versions that don't have tasklet.throw.
    Note, that delivery in those cases is always immediate (pending==False).
    """
    if hasattr(tasklet, "throw"):
        return tasklet.throw(exc, val, tb, pending)
    #currently, channel.send_exception allows only (type, arg1, ...)
    #and can"t cope with tb
    if exc is None:
        if val is None:
            val = sys.exc_info()[1]
        exc = val.__class__
    elif val is None:
        if isinstance(type, exc):
            exc, val = exc, ()
        else:
            exc, val = exc.__class__, exc
    if not isinstance(val, tuple):
        val = val.args
    tasklet.raise_exception(exc, *val)

class ChannelSequenceMixin(object):
    """
    A mixin that adds the channel sequence operations on top of the more simple
    channel operations.  Useful when building custom channels.
    """

    def send_sequence(self):
        for i in sequence:
            self.send(i)

    def __iter__(self):
            return self

    def __next__(self):
        try:
            return self.receive()
        except ValueError as e:
            if "closed channel" in str(e):
                raise StopIteration
            raise

class QueueChannel(ChannelSequenceMixin, stackless.channel):
    """
    A QueueChannel is like a channel with a queue for holding data.  The queue has
    a 'max_len' value.  If it is negative, the queue can grow forever.
    If the balance is zero or positive, if there is room on the queue, a sender
    will not block but have its data added to the queue.
    If the queue is full, a sender will block
    until its data can be added to the queue.
    If the balance is negative, it behaves like a normal channel.
    """
    def __init__(self, max_len=-1):
        """
        Initialize the QueueChannel with a max_len.  The default is -1 which means
        that it is unlimited.
        """
        self.value_queue = collections.deque()
        self.max_len = max_len

    @property
    def balance(self):
        return len(self.value_queue) + super(QueueChannel, self).balance

    def _send(self, value):
        # returns true if a send should append its result to the
        # queue
        sup = super(QueueChannel, self)
        with atomic():
            if not sup.closing and sup.balance == 0:
                if self.max_len < 0 or len(self.value_queue) < self.max_len:
                    self.value_queue.append(value)
                    return
            sup.send(value)

    def send(self, data):
        self._send((True, data))

    def send_exception(self, exc, *args):
        self.send_throw(exc, args)

    def send_throw(self, exc, value=None, tb=None):
        """call with similar arguments as raise keyword"""
        self._send((False, (exc, value, tb)))

    def _nb_receive(self, sup):
        # receive from channel wihout blocking.  Need
        # to temporarily change the channel behaviour
        assert(sup.balance > 0)
        old = self.preference, self.schedule_all
        self.preference, self.schedule_all = -1, False
        value = sup.receive()
        self.preference, self.schedule_all = old
        return value

    def receive(self):
        sup = super(QueueChannel, self)
        with atomic():
            # is there data on the channel? move it to the queue
            if sup.balance > 0:
                self.value_queue.append(self._nb_receive(sup))
            if self.value_queue:
                value = self.value_queue.popleft()
            else:
                value = sup.receive()
            ok, data = value
            if ok:
                return data
            exc, value, tb = data
            try:
                #raise exc, value, tb
                raise exc.with_traceback(tb)
            finally:
                tb = None

def tasklet_new(function, args=(), kwargs={}):
    """
    A simple dispatcher which causes the function to start running on a new tasklet
    """
    return stackless.tasklet(function)(*args, **kwargs)

def tasklet_run(function, args=(), kwargs={}):
    """
    A simple dispatcher which causes the function to start running on a new tasklet
    and execute immediately
    """
    t = stackless.tasklet(function)(*args, **kwargs)
    t.run()
    return t

def tasklet_call(function, args=(), kwargs={},
        dispatcher=tasklet_run, timeout=None, on_abandoned=None):
    """Run the given function on a different tasklet and return the result.
       'dispatcher' must be a callable which, when called with with
       (func, args, kwargs) causes asynchronous execution of the function to commence.
       If a result isn't received within an optional time limit, a TimeoutError is raised.
       If the waiting tasklet is interrupted before the function returns, 'onOrphaned' is called.
       If the target tasklet is killed, a CancelledError is raised.
    """
    # use a regular channel with reader priority so that we get woken up promply.
    chan = stackless.channel()
    done = [False] # avoid local binding in 'helper'
    def helper():
        """This helper marshals the result value over the channel"""
        try:
            try:
                try:
                    result = function(*args, **kwargs)
                except TaskletExit as e:
                    raise CancelledError(*e.args)
                finally:
                    done[0] = True
            except BaseException:
                send_throw(chan, *sys.exc_info())
            else:
                chan.send(result)
        except (ValueError, StopIteration): # old versions raised StopIteration
            pass # The originator is no longer listening

    # submit the helper to the dispatcher
    dispatcher(helper)
    # wait for the result
    with atomic():
        try:
            return channel_wait(chan, timeout)
        finally:
            chan.close()
            if on_abandoned and not done[0]:
                on_abandoned()


# A timeout context manager
# First, a hidden inner exception that is not caught by normal exception handlers
class _InternalTimeout(BaseException):
    pass

@contextlib.contextmanager
def timeout(delay, blocked=False, exc=None):
    """
    A context manager which installes a timeout handler and will cause a
    TimeoutError to be raised on the tasklet if it is triggered.
    if "blocked" is true, then the timeout will only occur if the tasklet
    is blocked on a channel.
    "exc" can be an exception class or an exception instance to raise,
    otherwise, TimeoutError is raised.
    """
    if delay is None or delay < 0:
        # The infinite timeout case
        yield
        return

    # waiting_tasklet is used as a senty to show that the original
    # caller is still in the context manager
    waiting_tasklet = stackless.getcurrent()
    inst = object() # Create a unique instance

    def old_callback():
        with atomic():
            if waiting_tasklet: # it is in the timeout context still
                if blocked and not waiting_tasklet.blocked:
                    return
                waiting_tasklet.raise_exception(_InternalTimeout, inst)

    def callback():
        with atomic():
            if waiting_tasklet: # it is in the timeout context still
                if blocked and not waiting_tasklet.blocked:
                    return # Don't timeout a non-blocked tasklets
                try:
                    waiting_tasklet.throw(_InternalTimeout(inst), pending=True)
                except AttributeError:
                    # tasklet.throw is new. Fallback to raise_exception
                    # raise_exception is immediate, so we must call it on a tasklet
                    stackless.tasklet(old_callback)()

    def delayed_callback():
        # call the callback from a worker
        stackless.tasklet(callback)()

    with atomic():
        handle = app.event_queue.call_later(delay, callback)
        try:
            yield # Run the code
        except _InternalTimeout as e:
            # Check if it is _our_ exception instance:
            if e.args[0] is inst:
                # Turn it into the proper timeout
                handle = None
                # construct exception
                if exc is None:
                    exc = TimeoutError("timed out after %ss"%(delay,))
                else:
                    if not isinstance(exc, BaseException):
                        exc = exc() #instantiate it
                raise exc(None).with_traceback( sys.exc_info()[2])
            raise # it is someone else's error
        finally:
            waiting_tasklet = None
            if handle:
                handle.cancel()
_timeout = timeout #to resolve conflict with local variables

def timeout_call(function, delay):
    """A call wrapper, returning (success, result), where "success" is true if there was no timeout"""
    try:
        with timeout(delay):
            return True, function()
    except TimeoutError as e:
        return False, e

def timeout_function(delay):
    """A decorator applying the given timeout to a function"""
    def helper(function):
        @contextlib.wraps(function)
        def wrapper(*args, **kwargs):
            with timeout(delay):
                return function(*args, **kwargs)
        return wrapper
    return helper

class Timeouts(object):
    def __init__(self, delay, blocked=False, exc=None):
        self.blocked = blocked
        self.exc = exc
        if delay is not None and delay >= 0:
            self.deadline = time() + delay
        else:
            self.deadline = None

    def delay(self):
        if self.deadline is not None:
            return self.deadline - time()

    def timeout(self):
        delay = self.delay()
        if delay is not None and delay <= 0.0 and not self.blocked:
            # raise the timeout error here
            if self.exc:
                raise self.exc
            else:
                raise TimeoutError
        return _timeout(delay, self.blocked, self.exc)


class _InternalCancel(BaseException):
    """Used internally to signal cancel"""

class cancellable(object):
    """A context manager that serves as a handle to cancel tasklets."""
    def __init__(self):
        self.tasklet = None
        self.exception = None

    def __enter__(self):
        assert self.tasklet is None # recursion not permitted
        self.tasklet = stackless.getcurrent()
        return self

    def __exit__(self, exc, val, tb):
        if exc is _InternalCancel and val.args[0] is self:
            assert self.tasklet is False
            self.exception = CancelledError(*val.args[1])
            raise self.exception(None).with_traceback( tb)
        else:
            assert self.tasklet is stackless.getcurrent()
            self.tasklet = None

    def cancel(self, *args):
        with atomic():
            t = self.tasklet
            if t:
                self.tasklet = False # Signal cancellation
                t.raise_exception(_InternalCancel, self, args)

    def cancelled(self):
        return self.tasklet is False

    def match(self, val):
        return self.exception is not None and self.exception is val
