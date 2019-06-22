import deltasigma
import numpy as np

class ExtractRidgePoint:
    def __init__(self):
        self.THRESHOLD = 0.5
        self.none_zero_index = list()

        # remove isolated points
        self.iterations = 3
        self.DIM_MAX = 5
        self.DIM_MIN = 2

        self.point_x = list()
        self.point_y = list()

    def execute_ridge_point_extraction(self, fx, fy, frangied_img):
        Fx_1 = deltasigma.circshift(fx, [0, -1])  # fx in -X direction
        print("sdsd", Fx_1)

        Fy_1 = deltasigma.circshift(fy, [0, -1])  # fy in -X direction
        Fx_2 = deltasigma.circshift(fx, [0, 1])  # fx in +X direction
        Fy_2 = deltasigma.circshift(fy, [0, 1])  # fy in +X direction
        Fx_3 = deltasigma.circshift(fx, [-1, 0])  # fx in -Y direction
        Fy_3 = deltasigma.circshift(fy, [-1, 0])  # fy in -Y direction
        Fx_4 = deltasigma.circshift(fx, [1, 0])  # fx in +Y direction
        Fy_4 = deltasigma.circshift(fy, [1, 0])  # fy in +Y direction

        Ta = 0.
        Fx_ridge = np.dot((fx > 0),
                          ((np.dot(fx, Fx_1) + np.dot(fy, Fy_1) < Ta).any() and (np.dot(fx, Fx_2) + np.dot(fy, Fy_2) > Ta).any()))
        Fy_ridge = np.dot((fy > 0).all(),
                          ((np.dot(fx, Fx_3) + np.dot(fy, Fy_3) < Ta).any() and (np.dot(fx, Fx_4) + np.dot(fy, Fy_4) > Ta).any()))


        # Truncate the boundary output
        a, b = frangied_img.shape
        m1 = 2
        m2 = 2
        MaskRidgePoint = np.ones([a, b])
        MaskRidgePoint[1:m1, :] = 0
        MaskRidgePoint[a - m1 + 1: a, :] = 0
        MaskRidgePoint[:, 1: m2] = 0
        MaskRidgePoint[:, b - m2 + 1: b] = 0

        RidgePointINDs = np.where((Fx_ridge.any() or Fy_ridge.any()) and MaskRidgePoint.any() > 0)
        px, py = self.ind2sub([a, b], np.array(RidgePointINDs))
        result = []
        for i in range(len(px)):
            result.append((px[i], py[i]))
        print(result)
        return result

    def ind2sub(self, array_shape, ind):
        ind[ind < 0] = -1
        ind[ind >= array_shape[0] * array_shape[1]] = -1
        rows = (ind.astype('int') / array_shape[1])
        cols = ind % array_shape[1]
        return rows, cols

