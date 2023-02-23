# CENG 487 Assignment3
# Talha Arık
# 270201060
# 11 2022

import sys
from vec3d import Vector3d


class InputOperations:
    def __init__(self):
        self.contents = []

    def read_file(self):
        with open(sys.argv[1], 'r') as f:
            self.contents = f.readlines()

    def parsing(self):
        vertices = []
        faces = []
        for i in self.contents:
            if i[0] == 'v':
                temporary_line = i.split()
                vertices.append(Vector3d(float(temporary_line[1]), float(temporary_line[2]), float(temporary_line[3]), 1.0))
            elif i[0] == 'f':
                temporary_faces = i.split()
                temporary_list = []
                for index, j in enumerate(temporary_faces):
                    if j == 'f':
                        continue
                    else:
                        temporary_list.append(vertices[int(j) - 1])
                faces.append(temporary_list)
        return vertices, faces
