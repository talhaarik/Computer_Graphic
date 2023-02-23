# CENG 487 Assignment2
# Talha Arık
# 270201060
# 11 2022

import math
import numpy as np


class Mat3d:

    def __init__(self):
        self.transform_matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    # Multiplies 4x4 and 4x1 matrices
    @staticmethod
    def multipy_matrices(matrix1, matrix2):
        result_matrix = [[0], [0], [0], [0]]

        for i in range(len(matrix1)):  # Iteration by row of matrix 1
            for j in range(len(matrix2[0])):  # Iteration by column by matrix 2
                for k in range(len(matrix2)):  # Iteration by rows of matrix2
                    result_matrix[i][j] += matrix1[i][k] * matrix2[k][j]
        return result_matrix

    #  Multiplies 4x4 and 4x4 matrices
    @staticmethod
    def multiply_matrices_for_transform(matrix1, matrix2):
        result_matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        for i in range(len(matrix1)):  # Iteration by row of matrix 1
            for j in range(len(matrix2[0])):  # Iteration by column by matrix 2
                for k in range(len(matrix2)):  # Iteration by rows of matrix2
                    result_matrix[i][j] += matrix1[i][k] * matrix2[k][j]
        return result_matrix

    @staticmethod
    def addition_matrix(matrix1, matrix2):
        result_matrix = [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
        return result_matrix

    @staticmethod
    def translation(tx, ty, tz):
        translation_matrix = [[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]]
        return translation_matrix

    # Returns rotation matrix. Only type for rotation angle. Once per axis and rotation.
    @staticmethod
    def rotation(x_axis, y_axis, z_axis):
        rotation_matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        if y_axis == 0 and z_axis == 0:
            rotation_matrix = [[1, 0, 0, 0],
                               [0, math.cos(math.radians(x_axis)), -(math.sin(math.radians(x_axis))), 0],
                               [0, math.sin(math.radians(x_axis)), math.cos(math.radians(x_axis)), 0],
                               [0, 0, 0, 1]]
        elif x_axis == 0 and z_axis == 0:
            rotation_matrix = [[math.cos(math.radians(y_axis)), 0, math.sin(math.radians(y_axis)), 0],
                               [0, 1, 0, 0],
                               [-(math.sin(math.radians(y_axis))), 0, math.cos(math.radians(y_axis)), 0],
                               [0, 0, 0, 1]]
        elif x_axis == 0 and y_axis == 0:
            rotation_matrix = [[math.cos(math.radians(z_axis)), -(math.sin(math.radians(z_axis))), 0, 0],
                               [math.sin(math.radians(z_axis)), math.cos(math.radians(z_axis)), 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]]
        return rotation_matrix

    @staticmethod
    def scale(sx, sy, sz):
        scale_matrix = [[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]]
        return scale_matrix

    def transpose_matrix(matrix):
        transpose_matrix = np.transpose(matrix)
        return transpose_matrix
