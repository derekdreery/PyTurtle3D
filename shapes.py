import pyglet
import numpy as np

class vec3(object):
    """simple 3D vector class"""
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, np.ndarray):
            if x.shape is not (3,):
                raise ValueError("vec3 must be length 3")
            self.vec = np.array(x, dtype='float32')
        elif isinstance(x, vec3):
            self.vec = np.array(x.vec)
        elif isinstance(x, list):
            if len(x) is not 3:
                raise ValueError("vec3 must be length 3")
            self.vec = np.array(x, dtype='float32')
        else:
            self.vec = np.array((x, y, z), dtype='float32')
        
    def translate(self, x=0, y=0, z=0):
        if isinstace(x, vec3):
            self.vec += x.vec
        else:
            self.vec += np.array((x, y, z))
        
    def rotate(self, q):
        if isinstance(q, quaternion):
            vec_in = quaternion(0, self.vec[0], self.vec[1], self.vec[2])
            self.vec = (q * vec_in * q.conj()).quat[1:].copy()
        else:
            raise NotImplemented
            
    def normalise(self):
        self.vec /= np.linalg.norm(self.vec)
    
    def __add__(self, vec_add):
        return vec3(self.vec + vec_add.vec)
        
    def __sub__(self, vec_sub):
        return vec3(self.vec - vec_sub.vec)
        
    def __mul__(self, mult):
        return vec3(self.vec * mult)
        
    def __rmul__(self, mult):
        return self.__mul__(mult)

    def __repr__(self):
        return "<shapes.vec3(%g, %g, %g) at 0x%x>" % (self.vec[0], \
                self.vec[1], self.vec[2], id(self))
                
    def __str__(self):
        return "(%.2g, %.2g, %.2g)" % (self.vec[0], self.vec[1], self.vec[2])

class quaternion(object):
    """Quaternian class"""
    def __init__(self, w=1, x=0, y=0, z=0):
        """Constructor can be numpy array, list, or individual parameters"""
        if isinstance(w, np.ndarray):
            if w.shape != (4,):
                raise IndexError("Quaternion from np.ndarray shape must be (4,)");
            self.quat = np.array(w, dtype='float32')
        elif isinstance(w, list):
            if len(w) != 4:
                raise IndexError("Quaternion from list len must be 4");
            self.quat = np.array(w, dtype='float32')
        else:
            self.quat = np.array((w,x,y,z), dtype='float32')
        
    def from_axis(self, vec, theta):
        """Create a quaternion from vec3 vec and angle theta"""
        sin_theta = np.sin(theta/2.)
        cos_theta = np.cos(theta/2.)
        v = vec3(vec).normalise()
        
        self.quat[1] = vec[0] * sin_theta
        self.quat[2] = vec[1] * sin_theta
        self.quat[3] = vec[2] * sin_theta
        self.quat[0] = cos_theta
        
    
    def normalise(self):
        TOL = 1e-5
        leng = sum(self.quat * self.quat)
        if abs(leng) > TOL and abs(leng - 1) > TOL:
            self.quat /= np.sqrt(leng)
        return self
    
    def __abs__(self):
        return np.linalg.norm(quat)
    
    def __add__(self, other):
        return quaternion(self.quat + other.quat)
        
    def __sub__(self, other):
        return quaternion(self.quat - other.quat)
        
    def __mul__(self, other):
        if not isinstance(other, quaternion):
            raise ValueError("Trying to mult quat with non quat")
        s = self.quat
        o = other.quat
        return quaternion([s[0]*o[0] - s[1]*o[1] - s[2]*o[2] + s[3]*o[3],
                           s[0]*o[1] + s[1]*o[0] + s[2]*o[3] - s[3]*o[2],
                           s[0]*o[2] - s[1]*o[3] + s[2]*o[0] + s[3]*o[1],
                           s[0]*o[3] + s[1]*o[2] - s[2]*o[1] + s[3]*o[0]])
    
    def conj(self):
        sq = self.quat
        return quaternion(sq[0], -sq[1], -sq[2], -sq[3])
    
    def __div__(self, other):
        return self * other.normalise().conj()
        
    def __repr__(self):
        return "<shapes.quaternion(w=%g, x=%g, y=%g, z=%g) at 0x%x" % \
                  (self.quat[0], self.quat[1], self.quat[2], self.quat[3], id(self))
    

class point(object):
    """
    Class that contains an object with location and direction
    
    Translation is relative to local coordinate space.
    """
    def __init__(self, x=0, y=0, z=0, r_x=0, r_y=0, r_z=0):
        self.pos = vec3(x,y,z)
        self.dir = vec3(r_x, r_y, r_z)

    def rotate(self, pitch=0, yaw=0, roll=0):
        """Change direction"""
        self.dir.x += pitch
        self.dir.y += yaw
        self.dir.z += roll
        
    def pitch(self, pitch):
        self.rotate(pitch=pitch)
        
    def yaw(self, yaw):
        self.rotate(yaw=yaw)
        
    def roll(self, roll):
        self.rotate(roll=roll)
        
    def move(self, x, y, z, coord_space='LOCAL'):
        if coord_space == 'LOCAL':
            self.pos.translate(x,y,z)
        elif coord_space == 'GLOBAL':
            self.pos.translate(x,y,z)
        

class vertex(object):
    """Class to handle a vertex on the path"""
    pass

class path(object):
    """class holding all the data for a turtle path"""
    def __init__(self):
        vertices = [vec3(),]
        
    def forward(self, amnt):
        pass
        
class turtle(object):
    def __init__(self):
        self.pos = vec3(0,0,0) #TODO
        self.dir = quaternion(1,0,0,0)
        
    def forward(self, distance):
        pass
        
    def rotate(self, pitch, yaw, roll):
        pass
        
    def pitch(self, angle, mode='degrees'):
        rotate(self, pitch=pitch, mode=mode)
        
    def yaw(self, angle, mode='degrees'):
        rotate(self, pitch=pitch, mode=mode)
        
    def roll(self, angle, mode='degrees'):
        rotate(self, pitch=pitch, mode=mode)

# end of file
