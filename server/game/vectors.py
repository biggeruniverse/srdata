# copyright (c) savagerebirth.com 2010
# a short vector class/module for use in some of the game-script replacements

# possible TODO: direction cosines relative to a given origin?
# other classmethods for other coordinate systems?

import math;

class Vec3:
	epsilon = 1e-6;
	
	def __init__(self, a=0, b=0, c=0):
		if isinstance(a, (list, tuple)):
			self.data = [float(x) for x in a];
		elif isinstance(a, Vec3):
			self.data = [a.data[0], a.data[1], a.data[2]];
		else:
			self.data = [float(a), float(b), float(c)];
	
	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False;
		#vectors are equal if and only if their components are equal
		return (
		  abs( self.data[0] - other.data[0]) < self.epsilon and 
		  abs( self.data[1] - other.data[1]) < self.epsilon and
		  abs( self.data[2] - other.data[2]) < self.epsilon
		);
	
	def __ne__(self, other):
		return not self.__eq__(other);
	
	def __add__ ( self, other):
		return self.__class__( self.data[0] + other.data[0], self.data[1] + other.data[1] , self.data[2] + other.data[2]);
	
	def __sub__( self, other):
		return self.__class__( self.data[0] - other.data[0], self.data[1] - other.data[1] , self.data[2] - other.data[2]);
	
	def __mul__(self, other):
		if isinstance( other, (int, float)): #scalar multiplication
			return self.__class__( other*self.data[0], other*self.data[1], other*self.data[2] );
		elif isinstance( other, Vec3): #dot product multiplication
			return self.dot(other);
		else:
			raise TypeError("Trying to multiply a Vec3 by something that's neither a vector nor a scalar.");
		
	def __div__(self, other):
		#note that scalar/vec 3 / (1,2,3) doesn't make (geometric) sense, so we only need to consider vec/scalar
		return self.__mul__(1/float(other));
	
	def __rmul__(self, other):
		#scalar multiplication and the dot product are commutitative
		return self.__mul__(other);
	
	def __neg__( self):
		return Vec3(-self.data[0], -self.data[1], -self.data[2]);
	
	def size(self):
		return math.sqrt(self.data[0]**2 + self.data[1]**2 + self.data[2]**2);

	def length(self):
		#alias for size
		return self.size();
	
	def normalise( self ):
		length = self.size(); #a float, make sure you don't normalise the zero vector
		if length > 0.0:
			#unrolling loops is faster
			self.data[0] /= length;
			self.data[1] /= length;
			self.data[2] /= length;
		return self;
	
	def dot( self, other):
		return self.data[0] * other.data[0] + self.data[1] * other.data[1] + self.data[2] * other.data[2];
	
	def cross( self, other): #self cross other
		return Vec3(
			self.data[1]*other.data[2] - self.data[2]*other.data[1] ,
			self.data[2]*other.data[0] - self.data[0]*other.data[2] ,
			self.data[0]*other.data[1] - self.data[1]*other.data[0]
		);
	
	def directionTo(self, other):
		return (other - self);
	
	def angleWith(self, other): #radians
		theta = self.dot(other) / (self.size() * other.size() ); #lengths will be floats
		return math.acos(theta);
	
	def getBearing( self ):
		#or the azimuth, if you prefer
		bearing = math.atan2(self.data[0], self.data[1]);
		bearing %= 2*math.pi;
		return math.degrees(bearing);
	
	#Spherical coordinates convention
	#theta: angle from the pole at the top of the sphere
	#phi: angle from the x axis. the direction directly from +x to +y is of increasing phi
	#NB getSpherical will returns theta in [0, pi] and phi in [-pi, pi]
	
	def getSpherical( self, origin=None):
		v = self if origin == None else self - origin;
		r = v.size();
		theta = math.acos( v.data[2]/r );
		phi = math.atan2(v.data[1],v.data[0]);
		
		return (r, phi, theta);
	
	@classmethod
	def fromSpherical(cls, r, phi, theta, origin=None):
		#the vector from 0,0,0 to (origin + the cartesian equivalent of r, phi, theta)
		if origin == None:
			origin = cls(0,0,0);
		x = r*math.cos(phi)*math.sin(theta);
		y = r*math.sin(phi)*math.sin(theta);
		z = r*math.cos(theta);
		v = cls(x, y, z);
		return v + origin;
	
	def distanceTo( self, other):
		#the distance between the points with self and other as position vectors
		return (self - other).size();
		
	def distanceSqTo( self, other):
		#the square of distanceTo, to save sqrt computation
		return (self.data[0] - other.data[0])**2 + (self.data[1] - other.data[1])**2 + (self.data[2] - other.data[2])**2;
	
	def __str__(self):
		return "[" +str(self.data[0]) + ", " +str(self.data[1])+ ", "+ str(self.data[2]) + "]";
	
	def __repr__(self):
		return "Vec3: " + self.__str__();
	
	def __iter__(self):
		return (c for c in self.data); #not a tuple comprehension but a generator comprehension!
	
	def __getitem__(self, i):
		return self.data[i];
	
	def __setitem__(self, i, value):
		self.data[i] = float(value);

e1 = Vec3(1,0,0);
e2 = Vec3(0,1,0);
e3 = Vec3(0,0,1);
zeroVec = Vec3(0,0,0);
origin = zeroVec;

def withinRange(a,b,dist):
	return a.distanceSqTo(b) <= dist**2;
