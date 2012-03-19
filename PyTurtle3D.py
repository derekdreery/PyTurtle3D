import pyglet
from pyglet.window import key
from pyglet.gl import *
from math import sin, cos, pi, radians

def vec(*args):
    return (GLfloat * len(args))(*args)

class vector3(object):
    """A class to handle vectors in 3 space, can handle rotated
       co-ordinates"""
    
    def __init__(self, x=0, y=0, z=0, rot_x=0, rot_y=90):
        self.x = x
        self.y = y
        self.z = z
        self.rot_x = rot_x % 360
        self.rot_y = rot_y % 180 - 90

    def move(self, x, y, z):
        self.x += (x * cos(radians(self.rot_x)) - z * sin(radians(self.rot_x))) * cos(radians(self.rot_y))
        self.z += (z * cos(radians(self.rot_x)) + x * sin(radians(self.rot_x))) * cos(radians(self.rot_y))
        self.y += -z * sin(radians(self.rot_y)) - y * cos(radians(self.rot_y))

    def rotate(self, x, y):
        self.rot_x += x
        self.rot_x %= 360
        if y + self.rot_y <= 90 and y + self.rot_y >= -90:
            self.rot_y += y


window = pyglet.window.Window()
#window.push_handlers(pyglet.window.event.WindowEventLogger())

class Cube(object):

    def __init__(self, x=0, y=0, z=0, color=(1.,1.,1.)):
        self.vertex_list = pyglet.graphics.vertex_list(24,
                       ('v3f', (x+1,y+1,z-1,
                                x-1,y+1,z-1,
                                x-1,y+1,z+1,
                                x+1,y+1,z+1,

                                x+1,y-1,z+1,
                                x-1,y-1,z+1,
                                x-1,y-1,z-1,
                                x+1,y-1,z-1,
                                
                                x+1,y+1,z+1,
                                x-1,y+1,z+1,
                                x-1,y-1,z+1,
                                x+1,y-1,z+1,
                                
                                x+1,y-1,z-1,
                                x-1,y-1,z-1,
                                x-1,y+1,z-1,
                                x+1,y+1,z-1,
                                
                                x-1,y+1,z+1,
                                x-1,y+1,z-1,
                                x-1,y-1,z-1,
                                x-1,y-1,z+1,
                                
                                x+1,y+1,z-1,
                                x+1,y+1,z+1,
                                x+1,y-1,z+1,
                                x+1,y-1,z-1
                                )),
                       ('c3f', color*24),
                       ('n3f', (0,1,0)*4 + \
                               (0,-1,0)*4 + \
                               (0,0,1)*4 + \
                               (0,0,-1)*4 + \
                               (1,0,0)*4 + \
                               (-1,0,0)*4))
                                


pos = vector3(0, 0, 0)
vel = vector3(0, 0, 0)
speed = 1
up = 0

cubes = []

for i in range(7):
    for j in range(7):
        for k in range(7):
            cubes.append(Cube(i*4, j*4, k*4, (i/7., j/7., k/7.)))

glShadeModel(GL_SMOOTH)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)

glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

@window.event
def on_resize(width, height):
    glViewport(0,0,width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65, width / float(height), .1, 1000)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
    #window.clear()
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glLoadIdentity()
    glRotatef(pos.rot_y, -1, 0, 0)
    glRotatef(pos.rot_x, 0, 1, 0)
    glTranslatef(pos.x, pos.y, pos.z - 5)
    
    glLightfv(GL_LIGHT0, GL_POSITION, vec(1,5,-20,0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(1,1,1,1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, vec(0.0,0.0,0.0,1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(0.5,0.5,0.5,1))
    
    #glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, vec(0,0,1,1))

    for cube in cubes:
        cube.vertex_list.draw(GL_QUADS)

@window.event
def on_key_press(symbol, modifiers):
    global speed, up
    if symbol == key.W:
        vel.z += 1
    if symbol == key.A:
        vel.x += 1
    if symbol == key.S:
        vel.z -= 1
    if symbol == key.D:
        vel.x -= 1
    if symbol == key.SPACE:
        up += 1
    if symbol == key.LSHIFT:
        speed *= 10
    if symbol == key.F:
        window.set_fullscreen(not window.fullscreen)

@window.event
def on_key_release(symbol, modifiers):
    global speed, up
    if symbol == key.W:
        vel.z -= 1
    if symbol == key.A:
        vel.x -= 1
    if symbol == key.S:
        vel.z += 1
    if symbol == key.D:
        vel.x += 1
    if symbol == key.SPACE:
        up -= 1
    if symbol == key.LSHIFT:
        speed /= 10

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    pos.rotate(dx/2., dy/2.)
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.RIGHT:
        window.set_exclusive_mouse(True)
    
@window.event
def on_mouse_release(x, y, button, modifiers):
    if button == pyglet.window.mouse.RIGHT:
        window.set_exclusive_mouse(False)

def update_camera(dt):
    global speed, up
    pos.move(vel.x*dt*speed, vel.y*dt*speed, vel.z*dt*speed)
    pos.y -= up*dt*speed
    print("(%f, %f, %f), (%f, %f)" % (pos.x, pos.y, pos.z, pos.rot_x, pos.rot_y))
        
pyglet.clock.schedule_interval(update_camera, 1/60.)

 
pyglet.app.run()
