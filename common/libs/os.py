# This is just a sub really


import sys, errno;

_names = sys.builtin_module_names

# Note:  more names are added to __all__ later.
__all__ = ["altsep", "sep", "extsep", "pathsep", "linesep",
           "defpath", "name", "path", "devnull"]

def _get_exports_list(module):
    try:
        return list(module.__all__)
    except AttributeError:
        return [n for n in dir(module) if n[0] != '_']

if 'posix' in _names:
    name = 'posix'
    linesep = '\n'
    from posix import *
    try:
        from posix import _exit
    except ImportError:
        pass
    import posixpath as path

    import posix
    __all__.extend(_get_exports_list(posix))
    del posix

elif 'nt' in _names:
    name = 'nt'
    linesep = '\r\n'
    from nt import *
    try:
        from nt import _exit
    except ImportError:
        pass
    import ntpath as path

    import nt
    __all__.extend(_get_exports_list(nt))
    del nt
else:
    raise ImportError('no os specific module found')

sys.modules['os.path'] = path
from os.path import (sep, pathsep, defpath, extsep, altsep,
    devnull)

del _names

def _exists(name):
    try:
        eval(name)
        return True
    except NameError:
        return False

if not _exists("_urandom"):
    def urandom(n):
        """urandom(n) -> str

        Return a string of n random bytes suitable for cryptographic use.

        """
        try:
            _urandomfd = open("/dev/urandom", O_RDONLY)
        except (OSError, IOError):
            raise NotImplementedError("/dev/urandom (or equivalent) not found")
        try:
            bs = b""
            while n > len(bs):
                bs += read(_urandomfd, n - len(bs))
        finally:
            close(_urandomfd)
        return bs
