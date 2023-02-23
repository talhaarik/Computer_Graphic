# CENG 487 Assignment2
# Talha Arık
# 270201060
# 11 2022

from mat3d import Mat3d
from vec3d import Vector3d


class Shape:

    def __init__(self):
        self.vertices_list = []
        self.transform_operations_list = []
        self.transform_matrix = Mat3d().transform_matrix

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
        for i in range(len(self.transform_operations_list)):  # Return self.transform_matrix.transform_matrix
            self.transform_matrix = Mat3d.multiply_matrices_for_transform(self.transform_matrix, self.remove_operations_list())

    #  Applies transformation to the vertices
    def transform(self):
        for i in range(len(self.vertices_list)):
            temp = Mat3d.multipy_matrices(self.transform_matrix, self.vertices_list[i].homogeneous_vector)
            self.vertices_list[i] = Vector3d(temp[0][0], temp[1][0], temp[2][0], temp[3][0])
