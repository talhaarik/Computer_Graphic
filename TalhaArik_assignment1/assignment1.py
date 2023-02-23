# CENG 487 Assignment1 by
# Talha Arık
# 270201060
# 10 2022

from vec3d import Vector3d
from mat3d import Mat3D
from shape import Shape
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

ESCAPE = '\033'  # I watched typing as '\033' from a video on the internet but unfortunately it doesn't work and I couldn't solve the problem
window = 0  # Number of the glut window.
triangle_shape = Shape()
square_shape = Shape()
mat3d_triangle = Mat3D()
mat3d_square = Mat3D()
transform_matrix_triangle = 0
transform_matrix_square = 0


def init_gl(width, height):
    global triangle_shape
    global square_shape
    global mat3d_triangle
    global mat3d_square

    glClearColor(0.0, 0.0, 0.0, 0.0)  # the background will be black
    glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

    #  Add vertices to shapes
    triangle_shape.adding_vertex(Vector3d(0.0, 1.0, 0.0, 1.0))
    triangle_shape.adding_vertex(Vector3d(1.0, -1.0, 0.0, 1.0))
    triangle_shape.adding_vertex(Vector3d(-1.0, -1.0, 0.0, 1.0))
    square_shape.adding_vertex(Vector3d(-1.0, 1.0, 0.0, 1.0))
    square_shape.adding_vertex(Vector3d(1.0, 1.0, 0.0, 1.0))
    square_shape.adding_vertex(Vector3d(1.0, -1.0, 0.0, 1.0))
    square_shape.adding_vertex(Vector3d(-1.0, -1.0, 0.0, 1.0))

    #  Perform the transformation
    square_shape.adding_operations_list(mat3d_square.rotation(0, 0, 5))
    triangle_shape.adding_operations_list(mat3d_triangle.rotation(0, 0, 5))

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset The Projection Matrix

    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)  # aspect ratio calculator
    glMatrixMode(GL_MODELVIEW)


#  Window resized
def resize_scene(width, height):  # When the screen is resized
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def construct_transform_matrix(shape, mat):
    transform_matrix = mat.transformation_matrix
    for i in range(len(shape.transform_operations_list)):
        transform_matrix = mat.multiply_matrices_for_transform(transform_matrix, shape.remove_operations_list())
    return transform_matrix


def transform(shape, matrix):
    for j in range(len(shape.vertices_list)):
        temp = Mat3D.multiplication_matrix_func(matrix, shape.vertices_list[j].homo_vector)
        shape.vertices_list[j] = Vector3d(temp[0][0], temp[1][0], temp[2][0], temp[3][0])


def draw_function():
    global triangle_shape
    global square_shape
    global transform_matrix_triangle
    global transform_matrix_square
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen and depth buffer
    glLoadIdentity()  # Reset The View
    glTranslatef(-1.5, 0.0, -6.0)  # Move Left 1.5 units and into the screen 6.0 units.

    glBegin(GL_POLYGON)  # Start drawing a polygon
    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex3f(triangle_shape.vertices_list[0].x, triangle_shape.vertices_list[0].y,
               triangle_shape.vertices_list[0].z)  # Top
    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex3f(triangle_shape.vertices_list[1].x, triangle_shape.vertices_list[1].y,
               triangle_shape.vertices_list[1].z)  # Bottom Right
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glVertex3f(triangle_shape.vertices_list[2].x, triangle_shape.vertices_list[2].y,
               triangle_shape.vertices_list[2].z)  # Bottom Left
    glEnd()  # Job done

    glTranslatef(3.0, 0.0, 0.0)  # Move Right 3.0 units.

    glColor3f(0.3, 0.5, 1.0)  # Bluish shade
    glBegin(GL_QUADS)  # Start drawing a 4 sided polygon
    glVertex3f(square_shape.vertices_list[0].x, square_shape.vertices_list[0].y,
               square_shape.vertices_list[0].z)  # Top Left
    glVertex3f(square_shape.vertices_list[1].x, square_shape.vertices_list[1].y,
               square_shape.vertices_list[1].z)  # Top Right
    glVertex3f(square_shape.vertices_list[2].x, square_shape.vertices_list[2].y,
               square_shape.vertices_list[2].z)  # Bottom Right
    glVertex3f(square_shape.vertices_list[3].x, square_shape.vertices_list[3].y,
               square_shape.vertices_list[3].z)  # Bottom Left
    glEnd()  # Job done

    #  Call transform function with related shape and transform matrix to perform transformation
    transform(square_shape, transform_matrix_square)
    transform(triangle_shape, transform_matrix_triangle)

    glutSwapBuffers()  # changing buffers


def key_pressed(*args):
    if args[0] == ESCAPE:
        sys.exit()


def main():
    # Defines global elements to use
    global window
    global triangle_shape
    global square_shape
    global mat3d_triangle
    global mat3d_square
    global transform_matrix_triangle
    global transform_matrix_square

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)  # Get a 640 x 480 window

    glutInitWindowPosition(0, 0)  # The window will start in the upper left corner of the screen
    window = glutCreateWindow("Talha Arik gururla sunar")
    glutDisplayFunc(draw_function)
    glutIdleFunc(draw_function)  # Redraw the scene while doing nothing
    glutReshapeFunc(resize_scene)  # When the window is resized
    glutKeyboardFunc(key_pressed)  # Record the function called when the keyboard is pressed.
    init_gl(640, 480)  # Initialize window.

    transform_matrix_triangle = construct_transform_matrix(triangle_shape,
                                                           mat3d_triangle)  # Construct transformation matrices
    transform_matrix_square = construct_transform_matrix(square_shape,
                                                         mat3d_square)  # Construct transformation matrices

    glutMainLoop()  # Start Event Processing Engine


print("Hit ESC key to quit.")
main()
