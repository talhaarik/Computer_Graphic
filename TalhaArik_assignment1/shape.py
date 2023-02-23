# CENG 487 Assignment1 by
# Talha Arık
# 270201060
# 10 2022

class Shape:
    def __init__(self):
        self.vertices_list = []
        self.transform_operations_list = []

    # Adds vertex to the shape
    def adding_vertex(self, vertices):
        self.vertices_list.append(vertices)

    # Removes vertex from shape
    def remove_vertex(self, vertices):
        self.vertices_list.remove(vertices)

    # Add matrix
    def adding_operations_list(self, matrix):
        self.transform_operations_list.append(matrix)

    # Remove matrix
    def remove_operations_list(self):
        current_matrix = self.transform_operations_list.pop()
        return current_matrix
