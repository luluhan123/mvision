import numpy as np
import cv2


class Threshold:
    def __init__(self):
        self.image = None
        self.low_threshold = 0.0
        self.high_threshold = 0.0

    def execute(self, image, low_threshold, high_threshold):
        ret = list()
        dim_x = image.shape[0]
        dim_y = image.shape[1]

        for i in range(dim_x):
            for j in range(dim_y):
                if (image[i,j] > low_threshold) & (image[i,j] < high_threshold):
                    ret.append([i, j])

        np_ret = np.array(ret)

        return self.remove_isolated_points(np_ret, 3)

    def remove_isolated_points(self, index, dim_max):
        count_none_zero_index = len(index)
        index_to_numpy = np.array(index)
        #index_to_numpy[:, [0, 1]] = index_to_numpy[:, [1, 0]]
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
