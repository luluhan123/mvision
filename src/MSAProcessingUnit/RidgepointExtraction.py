import numpy as np
import math


class RidgepointExtraction:
    def __init__(self):
        self.THRESHOLD = 0.5
        self.none_zero_index = list()

        # remove isolated points
        self.iterations = 3
        self.DIM_MAX = 5
        self.DIM_MIN = 2

        self.point_x = list()
        self.point_y = list()

        # set the parameters

    def set_iterations(self, iterations):
        self.iterations = iterations

    def set_max_dim(self, dim_max):
        self.DIM_MAX = dim_max

    def set_min_dim(self, dim_min):
        self.DIM_MIN = dim_min

    def execute_ridge_point_extraction(self, px, py, frangied_img):
        """
        - ridge point extraction
        :param px:
        :param py:
        :param frangied_img:
        :return:
        """
        xw, xh = px.shape
        yw, yh = py.shape
        x_type = px.dtype
        y_type = py.dtype

        # ----------    -x   ----------
        # initialize px_1,py_1
        left_shift_px = np.zeros(([xw, xh]), x_type)
        left_shift_py = np.zeros(([yw, yh]), y_type)

        # left shift
        left_shift_px[0:xw, xh - 1] = px[0:xw, 0]
        left_shift_px[0:xw, 0:xh - 1] = px[0:xw, 1:xh]
        left_shift_py[0:yw, yh - 1] = py[0:yw, 0]
        left_shift_py[0:yw, 0:yh - 1] = py[0:yw, 1:yh]

        # ----------- +x ---------------
        right_shift_px = np.zeros(([xw, xh]), x_type)
        right_shift_py = np.zeros(([yw, yh]), y_type)

        # right shift
        right_shift_px[0:xw, 0] = px[0:xw, xh - 1]
        right_shift_px[0:xw, 1:xh] = px[0:xw, 0:xh - 1]
        right_shift_py[0:yw, 0] = py[0:yw, yh - 1]
        right_shift_py[0:yw, 1:yh] = py[0:yw, 0:yh - 1]

        # ----------  -y ----------------
        up_shift_px = np.zeros(([xw, xh]), x_type)
        up_shift_py = np.zeros(([yw, yh]), y_type)

        # up shift
        up_shift_px[xw - 1, 0:xh] = px[0, 0:xh]
        up_shift_px[0:xw - 1, 0:xh] = px[1:xw, 0:xh]
        up_shift_py[yw - 1, 0:yh] = py[0, 0:yh]
        up_shift_py[0:yw - 1, 0:yh] = py[1:yw, 0:yh]

        # -----------  +y ---------------
        down_shift_px = np.zeros(([xw, xh]), x_type)
        down_shift_py = np.zeros(([yw, yh]), y_type)

        # down shift
        down_shift_px[0, 0:xh] = px[xw - 1, 0:xh]
        down_shift_px[1:xw, 0:xh] = px[0:xw - 1, 0:xh]
        down_shift_py[0, 0:yh] = py[yw - 1, 0:yh]
        down_shift_py[1:yw, 0:yh] = py[0:yw - 1, 0:yh]

        # -----------  top right corner ---------------
        top_right_shift_px = np.zeros(([xw, xh]), x_type)
        top_right_shift_py = np.zeros(([yw, yh]), y_type)

        # top left shift
        top_right_shift_px[0:xw, xh - 1] = px[0:xw, 0]
        top_right_shift_px[0:xw, 0:xh - 1] = px[0:xw, 1:xh]
        top_right_shift_py[0, 0:yh] = py[yw - 1, 0:yh]
        top_right_shift_py[1:yw, 0:yh] = py[0:yw - 1, 0:yh]

        # -----------  bottom left corner ---------------
        bottom_left_shift_px = np.zeros(([xw, xh]), x_type)
        bottom_left_shift_py = np.zeros(([yw, yh]), y_type)

        # top left shift
        bottom_left_shift_px[0:xw, 0] = px[0:xw, xh - 1]
        bottom_left_shift_px[0:xw, 1:xh] = px[0:xw, 0:xh - 1]
        bottom_left_shift_py[yw - 1, 0:yh] = py[0, 0:yh]
        bottom_left_shift_py[0:yw - 1, 0:yh] = py[1:yw, 0:yh]

        # -----------  top left corner ---------------
        top_left_shift_px = np.zeros(([xw, xh]), x_type)
        top_left_shift_py = np.zeros(([yw, yh]), y_type)

        # top right shift
        top_left_shift_px[0:xw, 0] = px[0:xw, xh - 1]
        top_left_shift_px[0:xw, 1:xh] = px[0:xw, 0:xh - 1]
        top_left_shift_py[0, 0:yh] = py[yw - 1, 0:yh]
        top_left_shift_py[1:yw, 0:yh] = py[0:yw - 1, 0:yh]

        # -----------  bottom right corner ---------------
        bottom_right_shift_px = np.zeros(([xw, xh]), x_type)
        bottom_right_shift_py = np.zeros(([yw, yh]), y_type)

        # top right shift
        bottom_right_shift_px[0:xw, xh - 1] = px[0:xw, 0]
        bottom_right_shift_px[0:xw, 0:xh - 1] = px[0:xw, 1:xh]
        bottom_right_shift_py[yw - 1, 0:yh] = py[0, 0:yh]
        bottom_right_shift_py[0:yw - 1, 0:yh] = py[1:yw, 0:yh]

        # Calculate all the ridges
        gradient_value_fx = px.copy()
        gradient_value_fy = py.copy()

        px[px > 0] = 1
        px[px < 0] = 0
        px = np.array(px, np.int8)

        py[py > 0] = 1
        py[py < 0] = 0
        py = np.array(py, np.int8)

        temp_left_shift = gradient_value_fx * left_shift_px + gradient_value_fy * left_shift_py
        temp_right_shift = gradient_value_fx * right_shift_px + gradient_value_fy * right_shift_py
        temp_up_shift = gradient_value_fx * up_shift_px + gradient_value_fy * up_shift_py
        temp_down_shift = gradient_value_fx * down_shift_px + gradient_value_fy * down_shift_py
        temp_top_right_shift = gradient_value_fx * top_right_shift_px + gradient_value_fy * top_right_shift_py
        temp_bottom_left_shift = gradient_value_fx * bottom_left_shift_px + gradient_value_fy * bottom_left_shift_py
        temp_top_left_shift = gradient_value_fx * top_left_shift_px + gradient_value_fy * top_left_shift_py
        temp_bottom_right_shift = gradient_value_fx * bottom_right_shift_px + gradient_value_fy * bottom_right_shift_py

        mt_threshold_tls = (temp_left_shift < self.THRESHOLD)
        lr_threshold_tls = (temp_left_shift > self.THRESHOLD)
        temp_left_shift[mt_threshold_tls] = 1
        temp_left_shift[lr_threshold_tls] = 0

        mt_threshold_trs = (temp_right_shift < self.THRESHOLD)
        lr_threshold_trs = (temp_right_shift > self.THRESHOLD)
        temp_right_shift[mt_threshold_trs] = 1
        temp_right_shift[lr_threshold_trs] = 0

        mt_threshold_tus = (temp_up_shift < self.THRESHOLD)
        lr_threshold_tus = (temp_up_shift > self.THRESHOLD)
        temp_up_shift[mt_threshold_tus] = 1
        temp_up_shift[lr_threshold_tus] = 0

        mt_threshold_tds = (temp_down_shift < self.THRESHOLD)
        lr_threshold_tds = (temp_down_shift > self.THRESHOLD)
        temp_down_shift[mt_threshold_tds] = 1
        temp_down_shift[lr_threshold_tds] = 0

        mt_threshold_ttrs = (temp_top_right_shift < self.THRESHOLD)
        lr_threshold_ttrs = (temp_top_right_shift > self.THRESHOLD)
        temp_top_right_shift[mt_threshold_ttrs] = 1
        temp_top_right_shift[lr_threshold_ttrs] = 0

        mt_threshold_tbls = (temp_bottom_left_shift < self.THRESHOLD)
        lr_threshold_tbls = (temp_bottom_left_shift > self.THRESHOLD)
        temp_bottom_left_shift[mt_threshold_tbls] = 1
        temp_bottom_left_shift[lr_threshold_tbls] = 0

        mt_threshold_ttls = (temp_top_left_shift < self.THRESHOLD)
        lr_threshold_ttls = (temp_top_left_shift > self.THRESHOLD)
        temp_top_left_shift[mt_threshold_ttls] = 1
        temp_top_left_shift[lr_threshold_ttls] = 0

        mt_threshold_tbrs = (temp_bottom_right_shift < self.THRESHOLD)
        lr_threshold_tbrs = (temp_bottom_right_shift > self.THRESHOLD)
        temp_bottom_right_shift[mt_threshold_tbrs] = 1
        temp_bottom_right_shift[lr_threshold_tbrs] = 0


        # calculate all the ridge point
        fx_ridge_point = px * (temp_left_shift * temp_right_shift)
        fy_ridge_point = py * (temp_up_shift * temp_down_shift)
        #right diagonal
        frd_ridge_point = px * py * (temp_top_right_shift * temp_bottom_left_shift)
        #left diagonal
        fld_ridge_point = px * py * (temp_top_left_shift * temp_bottom_right_shift)

        # do cut img boundary
        cut_img = self.cut_boundary(frangied_img)
        matrix_l = fx_ridge_point.shape[0]
        matrix_h = fx_ridge_point.shape[1]

        matrix_or = np.zeros(([matrix_l, matrix_h]), np.int8)

        for l in range(matrix_l):
            for h in range(matrix_h):
                matrix_or[l][h] = fx_ridge_point[l][h] or fy_ridge_point[l][h] or frd_ridge_point[l][h] or fld_ridge_point[l][h]

        # test num of matrix or
        count = 0
        for l in range(matrix_l):
            for h in range(matrix_h):
                if matrix_or[l][h] == 1:
                    count += 1
        # print("count", count)
        temp_threshold = np.max(frangied_img) * 0.1
        cut_img[cut_img > temp_threshold] = 1
        cut_img[cut_img < temp_threshold] = 0

        # find the index none-zero
        matrix_and = np.zeros(([matrix_l, matrix_h]))
        self.none_zero_index = list()
        for L in range(matrix_l):
            for H in range(matrix_h):
                matrix_and[L][H] = cut_img[L][H] and matrix_or[L][H]

                if matrix_and[L][H] == 1:
                    self.none_zero_index.append((L, H))

        self.none_zero_index.sort()

        result = self.remove_isolated_points(self.none_zero_index, self.DIM_MAX - 3)

        return result

    def remove_isolated_points(self, pts, dim_max):
        count_none_zero_index = len(pts)
        index_to_numpy = np.array(pts)
        index_to_numpy[:, [0, 1]] = index_to_numpy[:, [1, 0]]
        Dm = np.sqrt(np.sum((index_to_numpy - np.roll(index_to_numpy, -1, axis=0))**2, 1)).reshape(-1,1)
        Tm = (Dm > dim_max) & (Dm < dim_max+4)

        for i in range(2, Tm.size-1):
            Dn = np.sqrt(np.sum((index_to_numpy - np.roll(index_to_numpy, -i, axis=0))**2, 1)).reshape(-1,1)
            Dm = np.min(np.hstack([Dm, Dn]), axis=1).reshape(-1,1)
            Tn = (Dn > dim_max) & (Dn < dim_max+4)
            Tm = Tm | Tn

        term = (Dm <= dim_max) & Tm
        index_to_numpy[term.reshape(-1)].sort()
        return index_to_numpy[term.reshape(-1)]

    def execute_remove_isolated_points(self, index, dim_max):
        # self.point_x = list()
        # self.point_y = list()
        #
        # for point in index:
        #     self.point_x.append(point[1])
        #     self.point_y.append(point[0])

        count_none_zero_index = len(index)

        index_to_numpy = np.array(index)
        index_to_numpy[:, [0, 1]] = index_to_numpy[:, [1, 0]]

        up_shift_px = self.up_shift(index_to_numpy, 1)
        logical_and = self.calculate_the_logical_and(up_shift_px, dim_max)

        for n in range(2, count_none_zero_index + 1):
            iteration_up_shift = self.up_shift(index_to_numpy, n)
            up_shift_px = np.array([up_shift_px, iteration_up_shift]).min(0)
            iteration_logical_and = self.calculate_the_logical_and(iteration_up_shift, dim_max)
            logical_and = logical_and + iteration_logical_and

    def up_shift(self, index_to_numpy, n):

        xw, xh = index_to_numpy.shape
        up_shift_px = np.zeros(([xw, xh]), index_to_numpy.dtype)

        up_shift_px[xw - n:xw, 0:xh] = index_to_numpy[0:n, 0:xh]
        up_shift_px[0:xw - n, 0:xh] = index_to_numpy[n:xw, 0:xh]

        temp = (index_to_numpy - up_shift_px) ** 2
        up_shift = np.sqrt(temp[:, 0] + temp[:, 1])

        return up_shift

    def calculate_the_logical_and(self, up_shift_px, dim_max):

        temp_logical_by_max = up_shift_px.copy()
        temp_logical_by_min = up_shift_px.copy()

        flag_max_more = (temp_logical_by_max > dim_max)
        flag_max_less = (temp_logical_by_max <= dim_max)
        temp_logical_by_max[flag_max_more] = 1
        temp_logical_by_max[flag_max_less] = 0

        flag_min_less = (temp_logical_by_min < (dim_max + 4))
        flag_min_more = (temp_logical_by_min >= (dim_max + 4))
        temp_logical_by_min[flag_min_more] = 1
        temp_logical_by_min[flag_min_less] = 0

        matrix_and = temp_logical_by_max * temp_logical_by_min

        return matrix_and

    def cut_boundary(self, frangied_img):
        cut_img = frangied_img.copy()
        m, n = cut_img.shape
        weight = int(m*40/512)
        cut_img[0: m // weight, :] = 0
        cut_img[n - m // weight + 1:m, :] = 0

        cut_img[:, 0: n // weight] = 0
        cut_img[:, m - n // weight + 1] = 0
        return cut_img

    def truncate_boundary(self, frangied_img):
        cut_img = frangied_img.copy()
        a, b = cut_img.shape
        m1 = 2
        m2 = 2
        cut_img[1:m1, :] = 0
        cut_img[a - m1 + 1: a, :] = 0
        cut_img[:, 1: m2] = 0
        cut_img[:, b - m2 + 1: b] = 0
        return cut_img
