# CENG 487 Assignment3
# Talha Arık
# 270201060
# 11 2022


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from vec3d import Vector3d
from mat3d import Mat3d
from camera import Camera
from shape import Shape
from scene import Scene
from input_operations import InputOperations

window = 0  # Number of the glut window

# A general OpenGL initialization function.  Sets all the initial parameters.
def init_GL(width, height):
    global texture
    texture = glGenTextures(1)
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This will clear the background color to black
    glClearDepth(1.0)  # Enables clearing of the depth buffer
    glDepthFunc(GL_LESS)  # The type of depth test to do
    glEnable(GL_DEPTH_TEST)  # Enables depth testing
    glShadeModel(GL_SMOOTH)  # Enables smooth color shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset the projection matrix
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)  # Calculate the aspect ratio of the window
    glMatrixMode(GL_MODELVIEW)

# The function called when window is resized
def resize_GL_scene(width, height):
    if height == 0:  # If the window is too small
        height = 1

    glViewport(0, 0, width, height)  # Reset the current viewport and perspective transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The function called whenever a key is pressed.
def key_pressed(*args):
    if args[0] == GLUT_KEY_F1:  # If F1 is pressed, exit
        glutLeaveMainLoop()
    elif args[0] == GLUT_KEY_F2:  # If F2 is pressed, adds subdivison
        shape.add_subdivison()
    elif args[0] == GLUT_KEY_F3:  # If F3 is pressed, removes subdivison
        shape.remove_subdivison()
    elif args[0] == GLUT_KEY_LEFT:  # If left arrow is pressed, rotate left
        shape.adding_operations_list(Mat3d.rotation(0, -10, 0))
        shape.construct_transform_matrix()
        shape.transform()
    elif args[0] == GLUT_KEY_RIGHT:  # If right arrow is pressed, rotate right
        shape.adding_operations_list(Mat3d.rotation(0, 10, 0))
        shape.construct_transform_matrix()
        shape.transform()
    elif args[0] == GLUT_KEY_UP:  # If up arrow is pressed, rotate up
        shape.adding_operations_list(Mat3d.rotation(10, 0, 0))
        shape.construct_transform_matrix()
        shape.transform()
    elif args[0] == GLUT_KEY_DOWN:  # If down arrow is pressed, rotate down
        shape.adding_operations_list(Mat3d.rotation(-10, 0, 0))
        shape.construct_transform_matrix()
        shape.transform()


def main():
    global window
    global shape
    global scene
    global camera
    global camera_position
    global camera_front
    global camera_up

    scene = Scene()  # Initiate scene

    # Change coordinates of camera_position and camera_up to change camera properties
    camera_position = Vector3d(0, 0, 2, 1)
    camera_front = Vector3d(0, 0, -1, 1)
    camera_up = Vector3d(0, 1, 0, 1)

    camera = Camera(camera_position, Vector3d(0, 0, 0, 1), camera_up, camera_front)  # The second argument is for target. Change for target object. Add camera to the scene
    scene.add(camera)

    shape = Shape()  # Create a generic shape

    # Read shape from the file and add to the scene
    input_operation = InputOperations()
    input_operation.read_file()
    shape.vertices_list, shape.faces = input_operation.parsing()
    scene.add(shape)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Talha Arik sunar!")
    glutDisplayFunc(scene.draw_scene)
    glutIdleFunc(scene.draw_scene)
    glutReshapeFunc(resize_GL_scene)
    glutSpecialFunc(key_pressed)
    init_GL(640, 480)
    glutMainLoop()


print("Hit F1 key to quit.\n")
print("Operations: ")
print("=> Hit F2 to add subdivision")
print("=> Hit F3 to add subdivision")
print("=> Hit right arrow to rotate 10 degrees to the y axis")
print("=> Hit left arrow to rotate 10 degrees to the y axis")
print("=> Hit up arrow to rotate 10 degrees up")
print("=> Hit down arrow to rotate 10 degrees down")
main()
