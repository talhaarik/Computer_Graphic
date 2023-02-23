# CENG 487 Assignment3
# Talha Arık
# 270201060
# 11 2022

from vec3d import Vector3d
import numpy as np


class Camera:
    #  camera_position is the desired position of the camera
    #  camera_target is the target point
    #  camera_up is up vector that points towards the y-axis
    #  camera_front is showing the front of the camera
    def __init__(self, camera_position, camera_target, camera_up, camera_front):
        self.camera_position = camera_position

        temporary_direction = Vector3d(0, 0, 0, 0)
        temporary_direction.vector = list(np.array(camera_position.vector) - np.array(camera_target.vector))
        self.camera_direction = Vector3d(temporary_direction.vector[0] / temporary_direction.norm(), temporary_direction.vector[1] / temporary_direction.norm(), temporary_direction.vector[2] / temporary_direction.norm(), 0)

        temporary_right_axis = Vector3d(0, 0, 0, 0)
        temporary_right_axis.vector = (camera_up.cross_product_func(self.camera_direction))
        self.camera_right = Vector3d(temporary_right_axis.vector[0] / temporary_right_axis.norm(), temporary_right_axis.vector[1] / temporary_right_axis.norm(), temporary_right_axis.vector[2] / temporary_right_axis.norm(), 0)

        temporary_camera_up = Vector3d(0, 0, 0, 0)
        temporary_camera_up.vector = self.camera_direction.cross_product_func(self.camera_right)
        self.camera_up = Vector3d(temporary_camera_up.vector[0], temporary_camera_up.vector[1], temporary_camera_up.vector[2], 0)

        self.camera_front = camera_front
