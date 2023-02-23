# CENG 487 Assignment3
# Talha Arık
# 270201060
# 11 2022

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from camera import Camera
from shape import Shape


class Scene(object):

    def __init__(self):
        self.shape = None
        self.camera = None

    #  element is an object to add to scene.
    def add(self, element):
        if isinstance(element, Camera):
            self.camera = element
        elif isinstance(element, Shape):
            self.shape = element

    def draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(self.camera.camera_position.vector[0], self.camera.camera_position.vector[1], self.camera.camera_position.vector[2],
                  self.camera.camera_position.summation_func(self.camera.camera_front)[0],
                  self.camera.camera_position.summation_func(self.camera.camera_front)[1],
                  self.camera.camera_position.summation_func(self.camera.camera_front)[2],
                  self.camera.camera_up.vector[0], self.camera.camera_up.vector[1], self.camera.camera_up.vector[2])

        glPolygonMode(GL_FRONT, GL_LINE)
        glPolygonMode(GL_BACK, GL_LINE)
        glTranslatef(0.0, 0.0, -5.0)
        self.shape.draw()
        glRasterPos3f(-7, -5, -5.0)
        glutSwapBuffers()
