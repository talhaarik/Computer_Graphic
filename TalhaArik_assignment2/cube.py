# CENG 487 Assignment2
# Talha Arık
# 270201060
# 11 2022

import math
from vec3d import Vector3d
from shape import Shape
from OpenGL.GL import *


class Cube(Shape):

    def __init__(self):
        Shape.__init__(self)
        self.subdivision_list = [self.vertices_list]

    #  Function that add subdivison. Finds all the vertices of a planeand get middle points. Then, repeats for left points.
    def add_subdivison(self):
        temporary_sub_vertices = []
        for plane in self.subdivision_list:
            temp_plane = []
            center = Vector3d((plane[0].x + plane[2].x) / 2, (plane[0].y + plane[2].y) / 2, (plane[0].z + plane[2].z) / 2, 1)
            for index in range(len(plane)):
                v1 = Vector3d(0, 0, 0, 0)
                v2 = Vector3d(0, 0, 0, 0)
                v3 = Vector3d(0, 0, 0, 0)
                v4 = Vector3d(0, 0, 0, 0)
                temp_index = index + 1

                if index + 1 == len(plane):
                    temp_index = 0

                v1 = plane[index]

                v2.x = (plane[index].x + plane[temp_index].x) / 2
                v2.y = (plane[index].y + plane[temp_index].y) / 2
                v2.z = (plane[index].z + plane[temp_index].z) / 2
                v2.w = plane[index].w

                v3 = center

                v4.x = (plane[index].x + plane[index - 1].x) / 2
                v4.y = (plane[index].y + plane[index - 1].y) / 2
                v4.z = (plane[index].z + plane[index - 1].z) / 2
                v4.w = plane[index].w
                temporary_sub_vertices.append([v1, v2, v3, v4])

        self.subdivision_list = temporary_sub_vertices

    #  Function that removes subdivisions. It removes by finding predecessor points of midpoints
    def remove_subdivison(self):
        temporary_sub_vertices = []
        for index in range(0, len(self.subdivision_list) - 1, 4):
            v1 = Vector3d(0, 0, 0, 0)
            v2 = Vector3d(0, 0, 0, 0)
            v3 = Vector3d(0, 0, 0, 0)
            v4 = Vector3d(0, 0, 0, 0)

            v1.x = self.subdivision_list[index + 0][0].x
            v1.y = self.subdivision_list[index + 0][0].y
            v1.z = self.subdivision_list[index + 0][0].z
            v1.w = self.subdivision_list[index + 0][0].w

            v2.x = self.subdivision_list[index + 1][0].x
            v2.y = self.subdivision_list[index + 1][0].y
            v2.z = self.subdivision_list[index + 1][0].z
            v2.w = self.subdivision_list[index + 1][0].w

            v3.x = self.subdivision_list[index + 2][0].x
            v3.y = self.subdivision_list[index + 2][0].y
            v3.z = self.subdivision_list[index + 2][0].z
            v3.w = self.subdivision_list[index + 2][0].w

            v4.x = self.subdivision_list[index + 3][0].x
            v4.y = self.subdivision_list[index + 3][0].y
            v4.z = self.subdivision_list[index + 3][0].z
            v4.w = self.subdivision_list[index + 3][0].w

            temporary_sub_vertices.append([v1, v2, v3, v4])
        self.subdivision_list = temporary_sub_vertices

    #  Draw function to draw cube
    def draw_cube(self):
        for i in self.subdivision_list:
            glBegin(GL_QUADS)
            glColor3f(0.52, 0.566, 0.532)
            glVertex3f(i[0].x, i[0].y, i[0].z)
            glColor3f(0.3232, 0.532, 0.832)
            glVertex3f(i[1].x, i[1].y, i[1].z)
            glColor3f(3, 0.412, 0.911)
            glVertex3f(i[2].x, i[2].y, i[2].z)
            glColor3f(0.618, 0.312, 0.81)
            glVertex3f(i[3].x, i[3].y, i[3].z)
            glEnd()
