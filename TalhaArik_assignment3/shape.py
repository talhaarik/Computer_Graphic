# CENG 487 Assignment3
# Talha Arık
# 270201060
# 11 2022

from mat3d import Mat3d
from vec3d import Vector3d
from OpenGL.GL import *


class Shape:

    def __init__(self):
        self.vertices_list = []
        self.transform_operations_list = []
        self.transform_matrix = Mat3d().transform_matrix
        self.faces = []
        self.subdivision_level = 0

    #  Adds vertex to the shape
    def add_vertex(self, vertices):
        self.vertices_list.append(vertices)

    #  Removes vertex from shape
    def remove_vertex(self, vertices):
        self.vertices_list.remove(vertices)

    # Add matrix
    def adding_operations_list(self, matrix):
        self.transform_operations_list.append(matrix)

    # Remove matrix
    def remove_operations_list(self):
        current_matrix = self.transform_operations_list.pop()
        return current_matrix

    def construct_transform_matrix(self):
        self.transform_matrix = Mat3d().reset_transform_matrix()
        for i in range(len(self.transform_operations_list)):  # Return self.transform_matrix.transform_matrix
            self.transform_matrix = Mat3d.multiply_matrices_for_transform(self.transform_matrix, self.remove_operations_list())

    #  Applies transformation to the vertices
    def transform(self):
        for i in self.vertices_list:
            temporary = Mat3d.multiply_matrices(self.transform_matrix, i.homogeneous_vector)
            i.x = temporary[0][0]
            i.y = temporary[1][0]
            i.z = temporary[2][0]
            i.w = temporary[3][0]

    #  Function that adds subdivisions. Finds all vertices of the plane and gets their midpoints.
    def add_subdivison(self):
        temporary_sub_vertices = []
        for plane in self.faces:
            center = Vector3d(float((plane[0].x + plane[2].x) / 2), float((plane[0].y + plane[2].y) / 2), float((plane[0].z + plane[2].z) / 2), 1)
            for i in range(len(plane)):
                v2 = Vector3d(0, 0, 0, 0)
                v4 = Vector3d(0, 0, 0, 0)
                temporary_index = i + 1

                if i + 1 == len(plane):
                    temporary_index = 0

                v1 = plane[i]

                v2.x = float((plane[i].x + plane[temporary_index].x) / 2)
                v2.y = float((plane[i].y + plane[temporary_index].y) / 2)
                v2.z = float((plane[i].z + plane[temporary_index].z) / 2)
                v2.w = plane[i].w

                v3 = center

                v4.x = float((plane[i].x + plane[i - 1].x) / 2)
                v4.y = float((plane[i].y + plane[i - 1].y) / 2)
                v4.z = float((plane[i].z + plane[i - 1].z) / 2)
                v4.w = plane[i].w
                temporary_sub_vertices.append([v1, v2, v3, v4])

                self.vertices_list.append(v1)
                self.vertices_list.append(v2)
                self.vertices_list.append(v3)
                self.vertices_list.append(v4)

        self.faces = temporary_sub_vertices
        self.subdivision_level += 1

    #  Function that removes subdivisions. It removes by finding predecessor points of midpoints
    def remove_subdivison(self):
        if self.subdivision_level != 0:
            temporary_sub_vertices = []
            for i in range(0, len(self.faces) - 1, 4):
                temporary_sub_vertices.append([self.faces[i + 0][0], self.faces[i + 1][0], self.faces[i + 2][0], self.faces[i + 3][0]])
            self.faces = temporary_sub_vertices
            self.subdivision_level -= 1
        else:
            print("No subdivision ")

    def draw(self):
        for i in self.faces:
            glBegin(GL_QUADS)
            glColor3f(0.0, 1.0, 1.0)
            for j in i:
                glVertex3f(j.x, j.y, j.z)
            glEnd()
