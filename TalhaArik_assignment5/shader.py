# CENG 487 Assignment 5 by Talha Arık
# 270201060
# 01/2023

from OpenGL.GL import *


class Shader:
    def __init__(self, shader_type, shader_code, shader_program):

        self.shader_id = None
        self.shader_program = shader_program

        # Read the shader code from the files

        # Compile the shaders

        if shader_type == GL_VERTEX_SHADER:
            self.shader_id = glCreateShader(GL_VERTEX_SHADER)

        elif shader_type == GL_FRAGMENT_SHADER:
            self.shader_id = glCreateShader(GL_FRAGMENT_SHADER)

        glShaderSource(self.shader_id, shader_code)
        glCompileShader(self.shader_id)

        glAttachShader(self.shader_program, self.shader_id)
        glLinkProgram(self.shader_program)

    def detach(self):
        glDetachShader(self.shader_program)

    def delete_shader(self):
        glDeleteShader(self.shader_program)

    def set_uniform(self, name_, value_):
        location = glGetUniformLocation(self.shader_program, name_)
        glUniform1f(location, value_)

    def set_uniforms(self, uniform_names, uniform_values):

        for name_, value_ in zip(uniform_names, uniform_values):
            location = glGetUniformLocation(self.shader_program, name_)
            if isinstance(value_, float):
                glUniform1f(location, value_)
            elif isinstance(value_, int):
                glUniform1i(location, value_)
            elif isinstance(value_, tuple) and len(value_) == 3:
                # Assume a vec3 value
                glUniform3f(location, *value_)
            else:
                raise ValueError(f"Unsupported uniform value: {value_}")

    def get_program_id(self):
        return self.shader_program
