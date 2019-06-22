import numpy as np
import cv2
from MSAProcessingUnit.Frangi import Frangi
from scipy import signal


class GVF:
    def __init__(self):
        self.iterations = 30
        self.MU = 0.14

    def execute_gvf(self, filtered_img):
        frangi_filtered_img = filtered_img

        # normalize the filtered_img to the range[0, 1]
        frangi_filtered_img_max = np.max(frangi_filtered_img)
        frangi_filtered_img_min = np.min(frangi_filtered_img)
        frangi_filtered_img = (frangi_filtered_img - frangi_filtered_img_min) / (frangi_filtered_img_max - frangi_filtered_img_min)

        # expanding image,take care of boundary condition
        expanded_img = self.bound_mirror_expand(frangi_filtered_img)

        # calculate the gradient of the edge map
        fx, fy = np.gradient(expanded_img)

        # initialize GVF to the gradient field
        gradient_dir_fx = fx.copy()
        gradient_dir_fy = fy.copy()

        # squared magnitude of the gradient field
        sqrtMagf = np.square(fx, fx) + np.square(fy, fy)

        # iteratively solve for the GVF u,v
        for k in range(self.iterations+1):

            gradient_dir_fx = self.BoundMirrorEnsure(gradient_dir_fx)

            gradient_dir_fy = self.BoundMirrorEnsure(gradient_dir_fy)

            laplace_gradient_dir_fx = cv2.Laplacian(gradient_dir_fx, -1, ksize=3)
            laplace_gradient_dir_fy = cv2.Laplacian(gradient_dir_fx, -1, ksize=3)
            # la_ul = self.laplacian(gradient_dir_fx)

            gradient_dir_fx = gradient_dir_fx + self.MU * 4 * laplace_gradient_dir_fx - np.dot(sqrtMagf,
                                                                                               gradient_dir_fx - fx)
            gradient_dir_fy = gradient_dir_fy + self.MU * 4 * laplace_gradient_dir_fy - np.dot(sqrtMagf,
                                                                                              gradient_dir_fy - fy)
        bound_mirror_shrink_fx = self.BoundMirrorShrink(gradient_dir_fx)
        bound_mirror_shrink_fy = self.BoundMirrorShrink(gradient_dir_fy)

        squ = np.square(bound_mirror_shrink_fx,
                        bound_mirror_shrink_fx) + np.square(bound_mirror_shrink_fy, bound_mirror_shrink_fy)
        mag = np.sqrt(squ)

        output_gradient_x_dire = np.zeros([mag.shape[0], mag.shape[1]])
        output_gradient_y_dire = np.zeros([mag.shape[0], mag.shape[1]])

        for i in range(mag.shape[0]):
            for h in range(mag.shape[1]):
                output_gradient_x_dire[i][h] = gradient_dir_fx[i][h] / mag[i][h] + 1e-10
                output_gradient_y_dire[i][h] = gradient_dir_fy[i][h] / mag[i][h] + 1e-10

        return output_gradient_x_dire, output_gradient_y_dire

    def do_frangi_img(self, input):
        frangi = Frangi()
        frangi.img = input
        return frangi.execute()

    def bound_mirror_expand(self, filtered_img):
        """
        - Boundary mirror
        """
        length, width = filtered_img.shape
        bound_mirror_expand_img = np.zeros([length + 2, width + 2])
        bound_mirror_expand_img[1:length, 1:width] = filtered_img[0:length - 1, 0:width - 1]

        # corner joint mirror
        bound_mirror_expand_img[0][0] = bound_mirror_expand_img[2][2]
        bound_mirror_expand_img[0][width + 1] = bound_mirror_expand_img[2][width - 1]
        bound_mirror_expand_img[length + 1][0] = bound_mirror_expand_img[length - 1][2]
        bound_mirror_expand_img[length + 1][width + 1] = bound_mirror_expand_img[length - 1][width - 1]

        # Boundary mapping
        bound_mirror_expand_img[1:width + 1, 0] = bound_mirror_expand_img[1:width + 1, 2]
        bound_mirror_expand_img[1:width + 1, length + 1] = bound_mirror_expand_img[1:width + 1, length - 1]
        bound_mirror_expand_img[0, 1:length + 1] = bound_mirror_expand_img[2, 1: length + 1]
        bound_mirror_expand_img[width + 1, 1: length + 1] = bound_mirror_expand_img[width - 1, 1:length + 1]

        return bound_mirror_expand_img

    def BoundMirrorEnsure(self, input_u):
        """
           -Iterative image
        """
        length, width = input_u.shape

        bound_mirror_ensure_img = input_u.copy()

        # corner joint mirror
        bound_mirror_ensure_img[0][0] = bound_mirror_ensure_img[2][2]
        bound_mirror_ensure_img[0][width - 1] = bound_mirror_ensure_img[2][width - 3]
        bound_mirror_ensure_img[length - 1][0] = bound_mirror_ensure_img[length - 3][2]
        bound_mirror_ensure_img[length - 1][width - 1] = bound_mirror_ensure_img[length - 3][width - 3]

    def BoundMirrorExpand(self, filtered_img):
        m, n = filtered_img.shape
        B = np.zeros([m + 2, n + 2])
        x, y = B.shape
        B[1:m + 1, 1:n + 1] = filtered_img
        # print(B)
        # B[0:m+2, 0:n+2] = B[2:m+1, 2:n+1]
        B[0][0] = B[2][2]
        B[0][y - 1] = B[2][y - 3]
        B[x - 1][0] = B[x - 3][2]
        B[x - 1][y - 1] = B[x - 3][y - 3]
        # left boundary
        B[1:x - 1, 0] = B[1:x - 1, 2]
        # right boundary
        B[1:x - 1, y - 1] = B[1:x - 1, y - 3]
        # top boundary
        B[0, 1:y - 1] = B[2, 1:y - 1]
        # down boundary
        B[x - 1, 1:y - 1] = B[x - 3, 1:y - 1]
        return B


    def BoundMirrorEnsure(self, img):
        x, y = img.shape
        B = img.copy()
        B[0][0] = B[2][2]
        B[0][y - 1] = B[2][y - 3]
        B[x - 1][0] = B[x - 3][2]
        B[x - 1][y - 1] = B[x - 3][y - 3]
        # print(B)
        # left boundary
        B[1:x - 1, 0] = B[1:x - 1, 2]
        # right boundary
        B[1:x - 1, y - 1] = B[1:x - 1, y - 3]
        # top boundary
        B[0, 1:y - 1] = B[2, 1:y - 1]
        # down boundary
        B[x - 1, 1:y - 1] = B[x - 3, 1:y - 1]
        return B

    def laplacian(self, input):
        """
          - laplace operator
        """
        src_u = np.array(input, np.double)
        kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        sharped_u = signal.convolve2d(src_u, kernel, mode="same")
        laplace_filtered_img = input - sharped_u
        return laplace_filtered_img

    def BoundMirrorShrink(self, img):
        m, n = img.shape
        shrink = np.zeros([m-2, n-2])
        shrink[0:m-2, 0:n-2] = img[1:m-1, 1:n-1]
        return shrink








