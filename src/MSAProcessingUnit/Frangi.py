import math
import numpy as np
import cv2
from vtk.util import numpy_support as nps
# from scipy.ndimage.filters import convolve


class Frangi:
    def __init__(self):
        # the range of sigmas used
        self.scale_range = np.array([1, 10])

        # step size between sigmas
        self.scale_step = 10

        # correction constant
        self.beta_one = 0.5
        self.beta_two = 15

        # the black ridge set to true and the light ridge set false
        self.bright = True
        self.img = None

    def set_scale_range(self,scale_range):
        self.scale_range = scale_range

    def set_scale_step(self,scale_step):
        self.scale_step = scale_step

    def set_beta_one(self,beta_one):
        self.beta_one = beta_one

    def set_beta_two(self,beta_two):
        self.beta_two = beta_two

    def set_image_handling(self, input):
        dim = input.GetDimensions()
        flat_v = nps.vtk_to_numpy(input.GetPointData().GetScalars())
        img = flat_v.reshape(dim[0], dim[1], dim[2])
        self.img = img[:, :, 0]

    def set_numpy_image(self, input):
        self.img = input

    def execute(self):
        # the multi_scale
        sigmas = range(self.scale_range[0], self.scale_range[1] + 1, self.scale_step)

        # make matrix to store all filtered image
        all_filtered_img = np.zeros([self.img.shape[0], self.img.shape[1], len(sigmas)])

        # frangi filter for all sigmas
        for i in range(0, len(sigmas)):

            # make 2D Hessian
            dxx, dxy, dyy = self.hessian(self.img, sigmas[i])

            # correct for scale
            dxx *= sigmas[i] ** 2
            dxy *= sigmas[i] ** 2
            dyy *= sigmas[i] ** 2

            # calculate eigenvalues and vectors
            Lambda2, Lambda1, Ix, Iy = self.eigenvalue_eigenvector_to_image(dxx, dxy, dyy)
            # when the denominator is zero set some similarity measures
            near_zeros = np.isclose(Lambda1, np.zeros(Lambda1.shape))
            Lambda1[near_zeros] = 2 ** (-52)

            # prepare parameters for the transfer function
            Rb = (Lambda2 / Lambda1) ** 2
            S2 = Lambda1 ** 2 + Lambda2 ** 2
            #print type(S2), math.sqrt(np.max(S2))
            beta = 2 * self.beta_one ** 2
            c = 2 * self.beta_two ** 2

            # compute the output image
            filtered_img = np.exp(-Rb / beta) * (np.ones(self.img.shape) - np.exp(-S2 / c))

            if self.bright:
                filtered_img[Lambda1 < 0] = 0
            else:
                filtered_img[Lambda1 > 0] = 0

            # store the results in 3D matrix
            all_filtered_img[:, :, i] = filtered_img.copy()

        # return the every pixel the value of the scale(sigma) with the maximun
        if len(sigmas) > 1:
            output_img = np.amax(all_filtered_img, axis=2)
            output_img = output_img.reshape(self.img.shape[0], self.img.shape[1], order='F')
        else:
            # output pixel value
            output_img = all_filtered_img.reshape(self.img.shape[0], self.img.shape[1], order='F')

        # normalization
        if np.amax(output_img) != 0:
            output_img = output_img / np.amax(output_img)
            dim = output_img.shape
            for i in range(dim[0]):
                for j in range(dim[1]):
                    if i > int(dim[0] - dim[0]*0.05) or i < int(dim[0]*0.05):
                        output_img[i][j] = 0.0
                    if j > int(dim[1] - dim[1]*0.05) or j < int(dim[1]*0.05):
                        output_img[i][j] = 0.0
        return output_img

    # Make 2D Hessian
    def hessian(self, img, scale):
        gauss_kernel_xx = np.zeros([6 * scale + 1, 6 * scale + 1])
        gauss_kernel_xy = np.zeros([6 * scale + 1, 6 * scale + 1])

        # construct kernel function
        for x in range(-3 * scale, 3 * scale + 1):
            for y in range(-3 * scale, 3 * scale + 1):
                gauss_kernel_xx[x + 3 * scale][y + 3 * scale] = 1 / (2 * math.pi * scale ** 4) * (x ** 2 / scale ** 2 - 1) * math.exp(-(x ** 2 + y ** 2) / (2 * float(scale) ** 2))
                gauss_kernel_xy[x + 3 * scale][y + 3 * scale] = 1 / (2 * math.pi * scale ** 6) * (x * y) * math.exp(-(x ** 2 + y ** 2) / (2 * float(scale) ** 2))
        gauss_kernel_yy = gauss_kernel_xx.conj().T

        dxx = cv2.filter2D(img, -1, gauss_kernel_xx)
        dxy = cv2.filter2D(img, -1, gauss_kernel_xy)
        dyy = cv2.filter2D(img, -1, gauss_kernel_yy)

        return dxx, dxy, dyy

    def eigenvalue_eigenvector_to_image(self, dxx, dxy, dyy):

        temp = np.zeros((self.img.shape[0], self.img.shape[1]), dtype=np.float)

        for l1 in range(self.img.shape[0]):
            for l2 in range(self.img.shape[1]):
                temp[l1][l2] = math.sqrt((float(dxx[l1][l2]) - float(dyy[l1][l2])) *
                                         (float(dxx[l1][l2]) - float(dyy[l1][l2])) + 4 * float(dxy[l1][l2]) * float(dxy[l1][l2]))

        # computer the eigen vectors of v1 and v2
        v2x = 2 * dxy
        v2y = dyy - dxx + temp

        # normalize
        normalize = np.sqrt(v2x ** 2 + v2y ** 2)
        i = np.isclose(normalize, np.zeros(normalize.shape))
        flag = np.invert(i)
        v2x[flag] = v2x[flag] / normalize[flag]
        v2y[flag] = v2y[flag] / normalize[flag]

        # the eigenvectors are orthogonal
        v1x = -v2y.copy()
        v1y = v2x.copy()

        # compute the eigenvalues
        mu1 = 0.5 * (dxx + dyy + temp)
        mu2 = 0.5 * (dxx + dyy - temp)

        flag2 = np.absolute(mu1) > np.absolute(mu2)

        Lambda1 = mu1.copy()
        Lambda1[flag2] = mu2[flag2]
        Lambda2 = mu2.copy()
        Lambda2[flag2] = mu1[flag2]

        Ix = v1x.copy()
        Ix[flag2] = v2x[flag2]
        Iy = v1y.copy()
        Iy[flag2] = v2y[flag2]

        return Lambda1, Lambda2, Ix, Iy

    # ----------------------------------------------------------------------------------
    def local_execute(self,input):
        sigmas = range(self.scale_range[0], self.scale_range[1] + 1, self.scale_step)
        all_filtered_img = np.zeros([input.shape[0], input.shape[1], len(sigmas)])
        for i in range(0, len(sigmas)):
            dxx, dxy, dyy = self.local_hessian(input, sigmas[i])

            dxx *= sigmas[i] ** 2
            dxy *= sigmas[i] ** 2
            dyy *= sigmas[i] ** 2

            Lambda2, Lambda1, Ix, Iy = self.local_eigenvalue_eigenvector_to_image(dxx, dxy, dyy, input)

            near_zeros = np.isclose(Lambda1, np.zeros(Lambda1.shape))
            Lambda1[near_zeros] = 2 ** (-52)

            Rb = (Lambda2 // Lambda1) ** 2
            S2 = Lambda1 ** 2 + Lambda2 ** 2
            beta = 2 * self.beta_one ** 2
            # self.beta_two = 0.5 * max(S2)
            c = 2 * self.beta_two ** 2

            filtered_img = np.exp(-Rb // beta) * (np.ones(input.shape) - np.exp(-S2 // c))

            if self.bright:
                filtered_img[Lambda1 < 0] = 0
            else:
                filtered_img[Lambda1 > 0] = 0

            all_filtered_img[:, :, i] = filtered_img.copy()

        if len(sigmas) > 1:
            output_img = np.amax(all_filtered_img, axis=2)
            output_img = output_img.reshape(input.shape[0], input.shape[1], order='F')
        else:
            output_img = all_filtered_img.reshape(input.shape[0], input.shape[1], order='F')

        output_img = (1.0 * 3.0 * output_img) // np.amax(output_img)

        return output_img

    def local_hessian(self, img, scale):
        gauss_kernel_xx = np.zeros([6 * scale + 1, 6 * scale + 1])
        gauss_kernel_xy = np.zeros([6 * scale + 1, 6 * scale + 1])

        for x in range(-3 * scale, 3 * scale + 1):
            for y in range(-3 * scale, 3 * scale + 1):
                gauss_kernel_xx[x + 3 * scale][y + 3 * scale] = 1 // (2 * math.pi * scale ** 4) * (
                x ** 2 // scale ** 2 - 1) * math.exp(-(x ** 2 + y ** 2) // (2 * float(scale) ** 2))
                gauss_kernel_xy[x + 3 * scale][y + 3 * scale] = 1 // (2 * math.pi * scale ** 6) * (x * y) * math.exp(
                    -(x ** 2 + y ** 2) // (2 * float(scale) ** 2))
        gauss_kernel_yy = gauss_kernel_xx.conj().T

        dxx = cv2.filter2D(img, -1, gauss_kernel_xx)
        dxy = cv2.filter2D(img, -1, gauss_kernel_xy)
        dyy = cv2.filter2D(img, -1, gauss_kernel_yy)

        # dxx = convolve(img, gauss_kernel_xx, mode='constant', cval=0.0)
        # dxy = convolve(img, gauss_kernel_xy, mode='constant', cval=0.0)
        # dyy = convolve(img, gauss_kernel_yy, mode='constant', cval=0.0)

        return dxx, dxy, dyy

    def local_eigenvalue_eigenvector_to_image(self, dxx, dxy, dyy, input):
        temp = np.zeros((input.shape[0], input.shape[1]), dtype=np.float)

        for l1 in range(input.shape[0]):
            for l2 in range(input.shape[1]):
                temp[l1][l2] = math.sqrt((float(dxx[l1][l2]) - float(dyy[l1][l2])) *
                                         (float(dxx[l1][l2]) - float(dyy[l1][l2])) + 4 * float(dxy[l1][l2]) * float(
                    dxy[l1][l2]))

        v2x = 2 * dxy
        v2y = dyy - dxx + temp

        normalize = np.sqrt(v2x ** 2 + v2y ** 2)

        i = np.isclose(normalize, np.zeros(normalize.shape))
        flag = np.invert(i)
        v2x[flag] = v2x[flag] // normalize[flag]
        v2y[flag] = v2y[flag] // normalize[flag]

        v1x = -v2y.copy()
        v1y = v2x.copy()

        mu1 = 0.5 * (dxx + dyy + temp)
        mu2 = 0.5 * (dxx + dyy - temp)

        flag2 = np.absolute(mu1) > np.absolute(mu2)

        Lambda1 = mu1.copy()
        Lambda1[flag2] = mu2[flag2]
        Lambda2 = mu2.copy()
        Lambda2[flag2] = mu1[flag2]

        Ix = v1x.copy()
        Ix[flag2] = v2x[flag2]
        Iy = v1y.copy()
        Iy[flag2] = v2y[flag2]

        return Lambda1, Lambda2, Ix, Iy
