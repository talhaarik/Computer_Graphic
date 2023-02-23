# CENG 487 Assignment 5 by Talha Arık
# 270201060
# 01/2023

import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import pi, sin, cos, sqrt, acos

from VBO import VBO
from vector import *
from matrix import *
from boundingbox import *
from defs import DrawStyle

__all__ = ['_Shape', 'Cube', 'DrawStyle']


class _Shape:
    def __init__(self, name, vertices, faces):
        self.vertices = vertices
        self.edges = []
        self.faces = faces
        self.colors = []
        self.obj2World = Matrix()
        self.drawStyle = DrawStyle.NODRAW
        self.wireOnShaded = False
        self.wireWidth = 2
        self.name = name
        self.fixedDrawStyle = False
        self.wireColor = ColorRGBA(0.7, 1.0, 0.0, 1.0)
        self.wireOnShadedColor = ColorRGBA(1.0, 1.0, 1.0, 1.0)
        self.bboxObj = BoundingBox()
        self.bboxWorld = BoundingBox()
        self.calcBboxObj()

    def calcBboxObj(self):
        for vertex in self.vertices:
            self.bboxObj.expand(vertex)

    def setDrawStyle(self, style):
        self.drawStyle = style

    def setWireColor(self, r, g, b, a):
        self.wireColor = ColorRGBA(r, g, b, a)

    def setWireWidth(self, width):
        self.wireWidth = width

    def draw(self):
        # Initialize vertex data
        vertexData = []
        for face in self.faces:
            for vertex in face:
                vertexData.extend([self.vertices[vertex].x, self.vertices[vertex].y, self.vertices[vertex].z])

        # Convert the data to numpy arrays
        vertexData = np.array(vertexData, dtype=np.float32)

        vbo = VBO()
        vbo.bind()
        vbo.set_vertex_attribute(component_count=3, bytelength=len(vertexData) * 4, data=vertexData)

        # Specify the layout of the vertex data
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        # Set the draw style
        if self.drawStyle == DrawStyle.FACETED or self.drawStyle == DrawStyle.SMOOTH:

            # Initialize the color data
            colorData = []
            for i, face in enumerate(self.faces):
                colorData.extend([self.colors[i].r, self.colors[i].g, self.colors[i].b])

            colorData = np.array(colorData, dtype=np.float32)

            # Create a buffer for the colors
            colorBuffer = VBO()
            colorBuffer.bind()
            colorBuffer.set_vertex_attribute(component_count=3, bytelength=len(colorData) * 4, data=colorData)

            # Specify the layout of the color data
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

            # Draw the polygon with glDrawArrays
            vbo.draw()

            # Disable the color attribute array
            glDisableVertexAttribArray(1)

        if self.drawStyle == DrawStyle.WIRE or self.wireOnShaded:
            # Set polygon mode to wireframe
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(self.wireWidth)
            # Draw the polygon with glDrawArrays
            vbo.draw()
        # Reset polygon mode to fill
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


    def Translate(self, x, y, z):
        translate = Matrix.T(x, y, z)
        self.obj2World = self.obj2World.product(translate)


class Cube(_Shape):
    def __init__(self, name, xSize, ySize, zSize, xDiv, yDiv, zDiv):
        vertices = []
        xStep = xSize / (xDiv + 1.0)
        yStep = ySize / (yDiv + 1.0)
        zStep = zSize / (zDiv + 1.0)

        # add corners

        # Add corners
        for z in [zSize / 2.0, -zSize / 2.0]:
            for y in [-ySize / 2.0, ySize / 2.0]:
                for x in [-xSize / 2.0, xSize / 2.0]:
                    vertices.append(Point3f(x, y, z))

        faces = [[0, 2, 3, 1], [4, 6, 7, 5], [4, 6, 2, 0], [1, 3, 7, 5], [2, 6, 7, 3], [4, 0, 1, 5]]

        _Shape.__init__(self, name, vertices, faces)
        self.drawStyle = DrawStyle.SMOOTH

        for i in range(0, len(faces) + 1):
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            self.colors.append(ColorRGBA(r, g, b, 1.0))
