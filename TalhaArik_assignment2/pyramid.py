# CENG 487 Assignment2
# Talha Arık
# 270201060
# 11 2022

import math
from vec3d import Vector3d
from shape import Shape
from OpenGL.GL import *


class Pyramid(Shape):

    def __init__(self):
        Shape.__init__(self)
        self.subdivision_list = [self.vertices_list]

    #  Function that adds subdivision. Finds all the vertices of a plane and gets middle points. Then, repeats for left points.
    def add_subdivision(self):
        temporary_sub_vertices = []
        for plane in self.subdivision_list:
            current_mids = []
            mid_m_01 = Vector3d(0, 0, 0, 0)
            mid_m_12 = Vector3d(0, 0, 0, 0)
            mid_m_20 = Vector3d(0, 0, 0, 0)

            mid_m_01.x = (plane[0].x + plane[1].x) / 2
            mid_m_01.y = (plane[0].y + plane[1].y) / 2
            mid_m_01.z = (plane[0].z + plane[1].z) / 2
            mid_m_01.w = plane[0].w

            mid_m_12.x = (plane[1].x + plane[2].x) / 2
            mid_m_12.y = (plane[1].y + plane[2].y) / 2
            mid_m_12.z = (plane[1].z + plane[2].z) / 2
            mid_m_12.w = plane[1].w

            mid_m_20.x = (plane[2].x + plane[0].x) / 2
            mid_m_20.y = (plane[2].y + plane[0].y) / 2
            mid_m_20.z = (plane[2].z + plane[0].z) / 2
            mid_m_20.w = plane[2].w

            current_mids = [mid_m_01, mid_m_12, mid_m_20]
            temporary_sub_vertices.append(current_mids)

            for index in range(len(current_mids)):
                v0 = Vector3d(0, 0, 0, 0)
                v1 = Vector3d(0, 0, 0, 0)
                v2 = Vector3d(0, 0, 0, 0)

                v0.x = plane[index].x
                v0.y = plane[index].y
                v0.z = plane[index].z

                v1.x = current_mids[index].x
                v1.y = current_mids[index].y
                v1.z = current_mids[index].z

                v2.x = current_mids[index - 1].x
                v2.y = current_mids[index - 1].y
                v2.z = current_mids[index - 1].z

                temporary_sub_vertices.append([v0, v1, v2])

        self.subdivision_list = temporary_sub_vertices

    #  Function that removes subdivisions. It removes by finding predecessor points of midpoints
    def remove_subdivison(self):
        temporary_sub_vertices = []
        for index in range(0, len(self.subdivision_list) - 1, 4):
            v0 = Vector3d(0, 0, 0, 0)
            v1 = Vector3d(0, 0, 0, 0)
            v2 = Vector3d(0, 0, 0, 0)

            v0.x = self.subdivision_list[index + 1][0].x
            v0.y = self.subdivision_list[index + 1][0].y
            v0.z = self.subdivision_list[index + 1][0].z
            v0.w = self.subdivision_list[index + 1][0].w

            v1.x = self.subdivision_list[index + 2][0].x
            v1.y = self.subdivision_list[index + 2][0].y
            v1.z = self.subdivision_list[index + 2][0].z
            v1.w = self.subdivision_list[index + 2][0].w

            v2.x = self.subdivision_list[index + 3][0].x
            v2.y = self.subdivision_list[index + 3][0].y
            v2.z = self.subdivision_list[index + 3][0].z
            v2.w = self.subdivision_list[index + 3][0].w

            temporary_sub_vertices.append([v0, v1, v2])

        self.subdivision_list = temporary_sub_vertices

    #  Draw function to draw cube
    def draw_pyramid(self):
        for i in self.subdivision_list:
            glBegin(GL_POLYGON)
            glColor3f(1, 0.5, 0.8)
            glVertex3f(i[0].x, i[0].y, i[0].z)
            glColor3f(1, 0.5, 0)
            glVertex3f(i[1].x, i[1].y, i[1].z)
            glColor3f(0.32, 0.5, 0.12)
            glVertex3f(i[2].x, i[2].y, i[2].z)
            glEnd()
