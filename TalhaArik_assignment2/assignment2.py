# CENG 487 Assignment2
# Talha Arık
# 270201060
# 11 2022

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import cube
import pyramid
from camera import Camera
from mat3d import Mat3d
from shape import Shape
from vec3d import Vector3d

ESCAPE = '\033'

cube_shape = cube.Cube()
pyramid_shape = pyramid.Pyramid()

window = 0  # Number of the glut window

# A general OpenGL initialization function.  Sets all the initial parameters.
def init_GL(width, height):
    global cube_shape
    global pyramid_shape
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This will clear the background color to black
    glClearDepth(1.0)  # Enables clearing of the depth buffer
    glDepthFunc(GL_LESS)  # The type of depth test to do
    glEnable(GL_DEPTH_TEST)  # Enables depth testing
    glShadeModel(GL_SMOOTH)  # Enables smooth color shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset the projection matrix

    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)  # Calculate the aspect ratio of the window
    glMatrixMode(GL_MODELVIEW)

    cube_shape.subdivision_list = [
        [Vector3d(1.0, -1.0, -1.0, 1.0), Vector3d(1.0, 1.0, -1.0, 1.0), Vector3d(-1.0, 1.0, -1.0, 1.0),
         Vector3d(-1.0, -1.0, -1.0, 1.0)],
        [Vector3d(1.0, -1.0, 1.0, 1.0), Vector3d(1.0, 1.0, 1.0, 1.0), Vector3d(-1.0, 1.0, 1.0, 1.0),
         Vector3d(-1.0, -1.0, 1.0, 1.0)],
        [Vector3d(1.0, -1.0, -1.0, 1.0), Vector3d(1.0, 1.0, -1.0, 1.0), Vector3d(1.0, 1.0, 1.0, 1.0),
         Vector3d(1.0, -1.0, 1.0, 1.0)],
        [Vector3d(-1.0, -1.0, 1.0, 1.0), Vector3d(-1.0, 1.0, 1.0, 1.0), Vector3d(-1.0, 1.0, -1.0, 1.0),
         Vector3d(-1.0, -1.0, -1.0, 1.0)],
        [Vector3d(1.0, 1.0, 1.0, 1.0), Vector3d(1.0, 1.0, -1.0, 1.0), Vector3d(-1.0, 1.0, -1.0, 1.0),
         Vector3d(-1.0, 1.0, 1.0, 1.0)],
        [Vector3d(1.0, -1.0, -1.0, 1.0), Vector3d(1.0, -1.0, 1.0, 1.0), Vector3d(-1.0, -1.0, 1.0, 1.0),
         Vector3d(-1.0, -1.0, -1.0, 1.0)]]

    pyramid_shape.subdivision_list = [
        [Vector3d(0.0, 1.0, 0.0, 1.0), Vector3d(-1.0, -1.0, 1.0, 1.0), Vector3d(1.0, -1.0, 1.0, 1.0)],
        [Vector3d(0.0, 1.0, 0.0, 1.0), Vector3d(-1.0, -1.0, 1.0, 1.0), Vector3d(0.0, -1.0, -1.0, 1.0)],
        [Vector3d(0.0, 1.0, 0.0, 1.0), Vector3d(0.0, -1.0, -1.0, 1.0), Vector3d(1.0, -1.0, 1.0, 1.0)],
        [Vector3d(-1.0, -1.0, 1.0, 1.0), Vector3d(0.0, -1.0, -1.0, 1.0), Vector3d(1.0, -1.0, 1.0, 1.0)]]


# The function called when window is resized
def resize_GL_scene(width, height):
    if height == 0:  # If the window is too small
        height = 1

    glViewport(0, 0, width, height)  # Reset the current viewport and perspective transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def draw_GL_scene():
    global camera
    global camera_position
    global camera_front
    global camera_up
    global camera_speed

    # Change coordinates of camera_position and camera_up to change camera properties
    camera_position = Vector3d(3, 3, 10, 1)
    camera_front = Vector3d(0, 0, -1, 1)
    camera_up = Vector3d(0, 1, 0, 1)
    camera_speed = 0.05

    camera = Camera(camera_position, Vector3d(0, 0, 0, 1),
                    camera_up)  # The second argument is for target. Change for target object

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen and the depth buffer
    glLoadIdentity()  # Reset The View

    gluLookAt(camera_position.vector[0], camera_position.vector[1], camera_position.vector[2],
              camera_position.summation_func(camera_front)[0], camera_position.summation_func(camera_front)[1],
              camera_position.summation_func(camera_front)[2],
              camera_up.vector[0], camera_up.vector[1], camera_up.vector[2])

    glPolygonMode(GL_FRONT, GL_LINE)
    glPolygonMode(GL_BACK, GL_LINE)

    glTranslatef(-1.5, 0.0, -6.0)
    cube_shape.draw_cube()
    glTranslatef(3.0, 0.0, 0.0)
    pyramid_shape.draw_pyramid()
    glutSwapBuffers()  # Swap the buffers


# The function called whenever a key is pressed.
def key_Pressed(key, x, y):
    global cube_shape
    global pyramid_shape
    if ord(key) == 27:  # If escape is pressed, kill everything.
        glutLeaveMainLoop()
        return
    elif ord(x) == 65:  # If plus is pressed, adds subdivison
        cube_shape.add_subdivison()
        pyramid_shape.add_subdivision()
    elif ord(y) == 66:  # If minus is pressed, removes subdivison
        cube_shape.remove_subdivison()
        pyramid_shape.remove_subdivison()


def main():
    global window

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowSize(640, 480)  # Get a 640 x 480 window

    glutInitWindowPosition(0, 0)  # Window starts from the top left corner of the screen

    window = glutCreateWindow("Talha Arik gururla sunar!!")

    glutDisplayFunc(draw_GL_scene)  # Register the drawing function with glut

    glutIdleFunc(draw_GL_scene)  # Redraw the scene while nothing is being done

    glutReshapeFunc(resize_GL_scene)  # Register the function called when the window is resized.

    glutKeyboardFunc(key_Pressed)  # Register the function called when the keyboard is pressed.

    init_GL(640, 480)  # Initialize the window.

    glutMainLoop()  # Start event processing engine


print("Hit ESC key to quit.")
main()
