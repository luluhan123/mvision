from PIL import Image
import numpy as np
import cv2
from numpy import *


class TensorVoting:
    def __init__(self):
        self.hehe = 0

    def execute(self, img):
        # print "tensor voting execute"
        Ix = img.copy()
        Iy = img.copy()
        for j in range(1, img.shape[1] - 1):
            Ix[:, j] = (img[:, j + 1] - img[:, j - 1]) / 2
        Ix[:, 0] = img[:, 1] - img[:, 0]
        Ix[:, img.shape[1] - 1] = img[:, img.shape[1] - 1] - img[:, img.shape[1] - 2]
        for i in range(1, img.shape[0] - 1):
            Iy[i,] = (img[i + 1,] - img[i - 1,]) / 2
        Iy[0, :] = img[1, :] - img[0, :]
        Iy[img.shape[0] - 1, :] = img[img.shape[0] - 1, :] - img[img.shape[0] - 2, :]

        Ix2 = Ix * Ix
        Iy2 = Iy * Iy
        Ixy = Ix * Iy
        T = np.zeros((2, 2), dtype='float')

        P_eigenvalue2 = np.zeros((img.shape[0], img.shape[1]), dtype='float')
        C_eigenvalue_eigenvalue = np.zeros((img.shape[0], img.shape[1]), dtype='float')

        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                T = np.array(([(Ix2[i, j], Ixy[i, j]), (Ixy[i, j], Iy2[i, j])]), dtype='float')
                a = T[0, 0]
                b = T[0, 1]
                d = T[1, 0]
                c = T[1, 1]
                eigenvalue1 = ((a + c) + ((a - c) ** 2 + 4 * (b ** 2)) ** 0.5) / 2
                eigenvalue2 = ((a + c) - ((a - c) ** 2 + 4 * (b ** 2)) ** 0.5) / 2

                if (eigenvalue1 < eigenvalue2):
                    eigenvalue = eigenvalue1
                    eigenvalue1 = eigenvalue2
                    eigenvalue2 = eigenvalue
                # theta = math.atan((a - eigenvalue1) / b)
                P_eigenvalue2[i, j] = eigenvalue2
                C_eigenvalue_eigenvalue[i, j] = eigenvalue1 - eigenvalue2

        P_max = np.amax(P_eigenvalue2)
        P_min = np.amin(P_eigenvalue2)
        C_max = np.amax(C_eigenvalue_eigenvalue)
        C_min = np.amin(C_eigenvalue_eigenvalue)
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                P_eigenvalue2[i, j] = (P_eigenvalue2[i, j] - P_min) / (P_max - P_min)
                C_eigenvalue_eigenvalue[i, j] = (C_eigenvalue_eigenvalue[i, j] - C_min) / (C_max - C_min)

        l=20

        for i in range(0, C_eigenvalue_eigenvalue.shape[0]):
            for j in range(0,l):
                C_eigenvalue_eigenvalue[i, j] = 0
            for j in range(C_eigenvalue_eigenvalue.shape[1]-l+1,C_eigenvalue_eigenvalue.shape[1]):
                C_eigenvalue_eigenvalue[i, j] = 0
        for j in range(0, C_eigenvalue_eigenvalue.shape[1]):
            for i in range(0,l):
                C_eigenvalue_eigenvalue[i, j] = 0
            for i in range(C_eigenvalue_eigenvalue.shape[0]-l+1,C_eigenvalue_eigenvalue.shape[0]):
                C_eigenvalue_eigenvalue[i, j] = 0

        return np.transpose(C_eigenvalue_eigenvalue)
