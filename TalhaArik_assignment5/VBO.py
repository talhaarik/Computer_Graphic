# CENG 487 Assignment 5 by Talha Arık
# 270201060
# 01/2023

from OpenGL.GL import *


class VBO:
    def __init__(self):
        self.vbo = glGenBuffers(1)
        self.component_count = 0  # Vec2, Vec3, Vec4
        self.vertex_count = 0

    def __del__(self):
        glDeleteBuffers(1, [self.vbo])

    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

    def unbind(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def set_vertex_attribute(self, component_count: int, bytelength: int,
                             data: any):
        self.component_count = component_count
        stride = 4 * self.component_count
        self.vertex_count = bytelength // stride
        glBufferData(GL_ARRAY_BUFFER, bytelength, data, GL_STATIC_DRAW)

    def set_buffer_parameters(self, bytelength,data):
        glBufferData(GL_ARRAY_BUFFER, bytelength, data, GL_STATIC_DRAW)

    def set_slot(self, slot: int):
        glEnableVertexAttribArray(slot)
        glVertexAttribPointer(slot, self.component_count, GL_FLOAT, GL_FALSE, 0, None)

    def draw(self) -> None:
        glDrawArrays(GL_QUADS, 0, self.vertex_count)
