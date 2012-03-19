import pyglet

class vec3(object):
    """3D Vector class"""
    def __init__(self, x=0, y=0, z=0, r_x=0, r_y=0, r_z=0):
        self.x = x
        self.y = y
        self.z = z
        self.r_x = r_x
        self.r_y = r_y
        self.r_z = r_z

class vertex(object):
    """Class to handle a vertex on the path"""
    pass

class path(object):
    """class holding all the data for a turtle path"""
    def __init__(self):
        vertices = [vec3(),]
        
    def forward(self, amnt)
