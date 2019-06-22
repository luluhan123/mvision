import math
import numpy as np
import cv2
from vtk.util import numpy_support as nps


class SURF:
    def __init__(self):
        self.img = None
        self.centre_x = 0
        self.centre_y = 0
        self.threshold_value = 0

    def set_threshold_value(self, threshold_value):
        self.threshold_value = threshold_value

    def set_image_to_numpy(self, input):
        dim = input.GetDimensions()
        flat_v = nps.vtk_to_numpy(input.GetPointData().GetScalars())
        img = flat_v.reshape(dim[0], dim[1], dim[2])
        self.img = img[:, :, 0]

    def execute_surf(self, img, threshold=250):
        surf = cv2.xfeatures2d.SURF_create(threshold)
        (kp, descs) = surf.detectAndCompute(img, None)
        return kp