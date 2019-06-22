import numpy as np


class DeIsolatedPoint:
    def __init__(self):
        self.iterations = 3
        self.DIM_MAX = 5
        self.DIM_MIN = 2
        self.point_x = list()
        self.point_y = list()

    def set_iterations(self, iterations):
        self.iterations = iterations

    def set_max_dim(self, dim_max):
        self.DIM_MAX = dim_max

    def set_min_dim(self, dim_min):
        self.DIM_MIN = dim_min

    def execute_remove_isolated_points(self, size, index, dim_max):
        self.point_x = list()
        self.point_y = list()

        for point in index:
            self.point_x.append(point[0])
            self.point_y.append(point[1])

        count_none_zero_index = len(self.point_x)
        index_to_numpy = np.array(index)

        xw, xh = index_to_numpy.shape
        x_type = index_to_numpy.dtype
        up_shift_px = np.zeros(([xw, xh]), x_type)

        # up shift
        up_shift_px[xw - 1, 0:xh] = index_to_numpy[0, 0:xh]
        up_shift_px[0:xw - 1, 0:xh] = index_to_numpy[1:xw, 0:xh]

        temp = (index_to_numpy - up_shift_px) ** 2
        temp_sqrt = np.sqrt(temp[:, 0] + temp[:, 1])

        temp_logical_by_max = temp_sqrt.copy()
        temp_logical_by_min = temp_sqrt.copy()

        flag_max_more = (temp_logical_by_max > dim_max)
        flag_max_less = (temp_logical_by_max < dim_max)
        temp_logical_by_max[flag_max_more] = 1
        temp_logical_by_max[flag_max_less] = 0

        flag_min_less = (temp_logical_by_min < dim_max + 4)
        flag_min_more = (temp_logical_by_min > dim_max + 4)
        temp_logical_by_min[flag_min_more] = 1
        temp_logical_by_min[flag_min_less] = 0

        matrix_and = temp_logical_by_max * temp_logical_by_min

        # for n in range(2, count_none_zero_index + 1):
        #     up_shift_px[xw - n:xw, 0:xh] = index_to_numpy[0:n-1, 0:xh]
        #     up_shift_px[0:xw - n, 0:xh] = index_to_numpy[n:xw, 0:xh]

        print matrix_and


