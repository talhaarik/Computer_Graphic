# CENG 487 Assignment2
# Talha Arık
# 270201060
# 11 2022

import math
import numpy as np


class Vector3d:

    def __init__(self, x, y, z, w):
        self.w = w
        self.vector = [x, y, z]
        self.homogeneous_vector = [[x], [y], [z], [w]]

    @property
    def x(self):  # Point from x-axis
        return self.vector[0]

    @property
    def y(self):  # Point from y-axis
        return self.vector[1]

    @property
    def z(self):  # Point from z-axis
        return self.vector[2]

    @property
    def homogeneous_point(self):  # Homogeneous Point
        return self.w

    # Sums given vector with the vector inside
    def summation_func(self, vector):
        result = [0, 0, 0]  # Initial
        for i in range(len(self.vector)):
            result[i] += self.vector[i] + vector.vector[i]
        return result

    # Dot product to given vector and inside one
    def dot_product_func(self, vector):
        return (self.vector[0] * vector.vector[0]) + (self.vector[1] * vector.vector[1]) + (
                    self.vector[2] * vector.vector[2])

    def norm(self):
        return math.sqrt((self.vector[0] * self.vector[0]) + (self.vector[1] * self.vector[1]) + (self.vector[2] * self.vector[2]))

    # Multiplies given vector with the inside one
    def multiply_func(self, vector):
        return self.dot_product_func(vector)

    def scalar_mult_func(self, p):
        return [x * p for x in self.vector]

    # Cross product to given vector and inside one
    def cross_product_func(self, vector):
        x_value = self.vector[1] * vector.vector[2] - self.vector[2] * vector.vector[1]
        y_value = self.vector[2] * vector.vector[0] - self.vector[0] * vector.vector[2]
        z_value = self.vector[0] * vector.vector[1] - self.vector[1] * vector.vector[0]
        return [x_value, y_value, z_value]

    # Projection of a vector onto vector
    def projection_func(self, vector):
        return vector.scalar_mult_func(self.dot_product_func(vector) / vector.dot(vector))

    # Return the angle in degree between two vectors
    def angle_between_vectors_func(self, vector):
        return math.radians(math.acos(self.dot_product_func(vector.vector) / (self.norm() * np.linalg.norm(vector.vector))))

    @x.setter
    def x(self, value):
        self.x = value

    @y.setter
    def y(self, value):
        self.y = value

    @z.setter
    def z(self, value):
        self.z = value
