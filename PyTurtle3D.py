import pyglet
from pyglet.window import key
from pyglet.gl import *
from math import sin, cos, pi, radians

class vector3(object):
    """A class to handle vectors in 3 space, can handle rotated
       co-ordinates"""
    
    def __init__(self, x=0, y=0, z=0, rot_x=0, rot_y=0):
        self.x = x
        self.y = y
        self.z = z
        self.rot_x = rot_x
        self.rot_y = rot_y

    def move(self, x, y, z):
        self.x += (x * cos(radians(self.rot_x)) - z * sin(radians(self.rot_x))) * cos(radians(self.rot_y))
        self.z += (z * cos(radians(self.rot_x)) + x * sin(radians(self.rot_x))) * cos(radians(self.rot_y))
        self.y += -z * sin(radians(self.rot_y))

    def rotate(self, x, y):
        self.rot_x += x
        self.rot_x %= 360
        self.rot_y += y
        self.rot_y %= 360


window = pyglet.window.Window()
#window.push_handlers(pyglet.window.event.WindowEventLogger())
fps_display = pyglet.clock.ClockDisplay()


pos = vector3(0, 0, 0)
vel = vector3(0, 0, 0)
speed = 1


glEnable(GL_DEPTH_TEST)

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
    
    for i in range(0, 20, 3):
        for j in range(0, 20, 3):
            glBegin(GL_QUADS);                	# Draw A Quad
            glColor3f(0.0,1.0,0.0);            # Set The Color To Green
            glVertex3f( j+1.0, i+1.0,-1.0);        	# Top Right Of The Quad (Top)
            glVertex3f(j-1.0, i+1.0,-1.0);        	# Top Left Of The Quad (Top)
            glVertex3f(j-1.0, i+1.0, 1.0);        	# Bottom Left Of The Quad (Top)
            glVertex3f( j+1.0, i+1.0, 1.0);        	# Bottom Right Of The Quad (Top)
            glColor3f(1.0,0.5,0.0);            # Set The Color To Orange
            glVertex3f( j+1.0,i-1.0, 1.0);        	# Top Right Of The Quad (Bottom)
            glVertex3f(j-1.0,i-1.0, 1.0);        	# Top Left Of The Quad (Bottom)
            glVertex3f(j-1.0,i-1.0,-1.0);        	# Bottom Left Of The Quad (Bottom)
            glVertex3f( j+1.0,i-1.0,-1.0);        	# Bottom Right Of The Quad (Bottom)
            glColor3f(1.0,0.0,0.0);            # Set The Color To Red
            glVertex3f( j+1.0,i+1.0, 1.0);        	# Top Right Of The Quad (Front)
            glVertex3f(j-1.0,i+1.0, 1.0);        	# Top Left Of The Quad (Front)
            glVertex3f(j-1.0,i-1.0, 1.0);        	# Bottom Left Of The Quad (Front)
            glVertex3f( j+1.0,i-1.0, 1.0);        	# Bottom Right Of The Quad (Front)
            glColor3f(1.0,1.0,0.0);            # Set The Color To Yellow
            glVertex3f( j+1.0,i-1.0,-1.0);        	# Top Right Of The Quad (Back)
            glVertex3f(j-1.0,i-1.0,-1.0);        	# Top Left Of The Quad (Back)
            glVertex3f(j-1.0, i+1.0,-1.0);        	# Bottom Left Of The Quad (Back)
            glVertex3f( j+1.0, i+1.0,-1.0);        	# Bottom Right Of The Quad (Back)
            glColor3f(0.0,0.0,1.0);            # Set The Color To Blue
            glVertex3f(j-1.0, i+1.0, 1.0);        	# Top Right Of The Quad (Left)
            glVertex3f(j-1.0, i+1.0,-1.0);        	# Top Left Of The Quad (Left)
            glVertex3f(j-1.0,i-1.0,-1.0);        	# Bottom Left Of The Quad (Left)
            glVertex3f(j-1.0,i-1.0, 1.0);        	# Bottom Right Of The Quad (Left)
            glColor3f(1.0,0.0,1.0);            # Set The Color To Violet
            glVertex3f( j+1.0, i+1.0,-1.0);        	# Top Right Of The Quad (Right)
            glVertex3f( j+1.0, i+1.0, 1.0);        	# Top Left Of The Quad (Right)
            glVertex3f( j+1.0,i-1.0, 1.0);        	# Bottom Left Of The Quad (Right)
            glVertex3f( j+1.0,i-1.0,-1.0);        	# Bottom Right Of The Quad (Right)
            glEnd();
	
    fps_display.draw()

@window.event
def on_key_press(symbol, modifiers):
    global speed
    if symbol == key.W:
        vel.z += 1
    if symbol == key.A:
        vel.x += 1
    if symbol == key.S:
        vel.z -= 1
    if symbol == key.D:
        vel.x -= 1
    if symbol == key.LSHIFT:
        speed *= 10
    if symbol == key.F:
        window.set_fullscreen(not window.fullscreen)

@window.event
def on_key_release(symbol, modifiers):
    global speed
    if symbol == key.W:
        vel.z -= 1
    if symbol == key.A:
        vel.x -= 1
    if symbol == key.S:
        vel.z += 1
    if symbol == key.D:
        vel.x += 1
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
    global speed
    pos.move(vel.x*dt*speed, vel.y*dt*speed, vel.z*dt*speed)
    #pos.x += vel.x * dt * speed
    #pos.y += vel.y * dt * speed
    #pos.z += vel.z * dt * speed
    print("(%f, %f, %f), (%f, %f)" % (pos.x, pos.y, pos.z, pos.rot_x, pos.rot_y))
        
pyglet.clock.schedule_interval(update_camera, 1/60.)

 
pyglet.app.run()
