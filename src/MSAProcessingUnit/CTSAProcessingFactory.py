from MSAProcessingUnit.Frangi import Frangi
from MSAProcessingUnit.PointSet2DFindCluster import PointSet2DFindCluster
from MSAProcessingUnit.PointSet2DCurveFitting import PointSet2DCurveFitting
from MSAProcessingUnit.PointSet2DConvexHull import PointSet2DConvexHull
from MSAProcessingUnit.SURF import SURF
from MSAProcessingUnit.Rpca import Rpca
from MSAProcessingUnit.GVF import GVF
from MSAProcessingUnit.TensorVoting import TensorVoting
from MSAProcessingUnit.Threshold import Threshold
from MSAProcessingUnit.RidgepointExtraction import RidgepointExtraction

import vtk
import numpy as np
from vtk.util import numpy_support as nps
import scipy.cluster.vq as scv


class CTSAProcessingFactory:
    def __init__(self):
        self.i = 0
        self.init_radius = 160
        self.partImg = None
        self.ptsInImage = list()
        self.gvf = GVF()
        self.ridgePointExtraction = RidgepointExtraction()

    def curve_fitting(self, pts, maximum_point_num__per_cluster, x, y, tolerant_area):
        pts_clustering = PointSet2DFindCluster()
        pts_clustering.set_point_set(pts)
        pts_clustering.set_minimum_point_number_per_cluster(maximum_point_num__per_cluster)
        pts_clustering.set_tolerant_area(tolerant_area)
        pts_clustering.set_area_size(x, y)
        pts_clustering.execute()

        pts_curve = PointSet2DCurveFitting()
        pts_curve.set_minimum_point_number_per_cluster(maximum_point_num__per_cluster)
        pts_curve.set_area_size(x, y)
        pts_curve.execute(pts_clustering.get_underlying_cluster())

        lines_predicted_points = pts_curve.get_longest_curve()

        # lines_convex_hull = PointSet2DConvexHull()
        # lines_convex_hull.set_lines_points_set(lines_predicted_points)
        # lines_convex_hull.set_explore_area(30)
        # lines_convex_hull.set_area_size(x, y)
        # lines_convex_hull.execute()
        #
        # mask = lines_convex_hull.get_value_matrix()
        # hull_edge_points = lines_convex_hull.create_hull_edge_points()

        # hull_edge_points = lines_convex_hull.get_hull_edge_points()
        return lines_predicted_points

    def do_curve_fitting(self, pts, maximum_point_num__per_cluster, x, y, tolerant_area):
        pts_clustering = PointSet2DFindCluster()
        pts_clustering.set_point_set(pts)
        pts_clustering.set_minimum_point_number_per_cluster(maximum_point_num__per_cluster)
        pts_clustering.set_tolerant_area(tolerant_area)
        pts_clustering.set_area_size(x, y)
        pts_clustering.execute()

        pts_curve = PointSet2DCurveFitting()
        pts_curve.set_minimum_point_number_per_cluster(maximum_point_num__per_cluster)
        pts_curve.set_area_size(x, y)
        pts_curve.execute(pts_clustering.get_underlying_cluster())

        lines_predicted_points = pts_curve.get_longest_curve()
        lines_convex_hull = PointSet2DConvexHull()
        lines_convex_hull.set_lines_points_set(lines_predicted_points)
        lines_convex_hull.set_explore_area(25)
        lines_convex_hull.set_area_size(x, y)
        lines_convex_hull.execute()
        mask = lines_convex_hull.get_value_matrix()
        hull_edge_points = lines_convex_hull.create_hull_edge_points()
        # hull_edge_points = lines_convex_hull.get_hull_edge_points()
        return lines_predicted_points.get_data_list()

    def do_predict_possible_points(self, pts):
        # instantiate clustering algorithm object
        pts_clustering = PointSet2DFindCluster()

        # configure parameters
        pts_clustering.set_point_set(pts)
        pts_clustering.set_minimum_point_number_per_cluster(20)
        pts_clustering.set_tolerant_area(30)
        # pts_clustering.set_curve_fit(False)
        # execute algorithm
        pts_clustering.execute()
        # get predicted points
        underlying_cluster = pts_clustering.get_underlying_cluster()

        return pts_clustering.get_centroid(underlying_cluster)

    def ridge_point_extraction_key_area(self, frangi_key_area):
        px, py = self.gvf.execute_gvf(frangi_key_area)
        return self.ridgePointExtraction.execute_ridge_point_extraction(px, py, frangi_key_area)

    def execute_ridge_point_extraction(self, input_img):
        frangi_filtered_img = self.enhance_guide_wire(input_img)
        frangi_filtered_img = frangi_filtered_img / np.max(frangi_filtered_img)
        px, py = self.gvf.execute_gvf(frangi_filtered_img)
        return self.ridgePointExtraction.execute_ridge_point_extraction(px, py, frangi_filtered_img)

    def execute_gvf(self, input_img):
        frangi_filtered_img = self.enhance_guide_wire(input_img)
        gvf = GVF()
        return gvf.execute_gvf(frangi_filtered_img)

    def execute_rpca(self, input_matrix):
        rpca = Rpca()
        return rpca.inexact_augmented_lagrange_multiplier(input_matrix)

    def surf_guide_wire(self, input):
        surf = SURF()
        surf.set_image_to_numpy(input)
        return surf.execute_surf()

    def surf_guide_wire_guide_wire(self, input):
        frangi = Frangi()
        frangi.set_image_handling(input)
        return frangi.execute()

    def enhance_local_guide_wire(self, input):
        local_frangi = Frangi()
        return local_frangi.local_execute(input)

    def frangi_img(self, img):
        frangi = Frangi()
        frangi.set_numpy_image(img)
        return frangi.execute()

    def san_ban_fu(self, img):
        return self.ridge_point_extraction_key_area(self.frangi_img(img))

    def tensor_voting(self, img):
        tv = TensorVoting()
        th = Threshold()
        return th.execute(tv.execute(img), 0.22, 0.32)

    def do_surf_processing(self, img, threshold=250):
        surf = SURF()
        key_point = list()
        pts = surf.execute_surf(img, threshold)
        for points in pts:
            (x, y) = points.pt
            key_point.append((x, y))

        key_point_in_numpy = np.array(key_point, dtype=int)
        return key_point_in_numpy

    def init_get_part_NPimage(self, input):
        img = input[(np.round(self.init_point[0]) - self.init_radius / 2):(np.round(self.init_point[0]) + self.init_radius / 2),
              (np.round(self.init_point[1]) - self.init_radius / 2):(np.round(self.init_point[1]) + self.init_radius / 2)]
        self.partImg = img
        return img

    def get_part_NPimage(self, input, center):
        img = input[(center[0] - self.init_radius / 2):(center[0] + self.init_radius / 2), (center[1] - self.init_radius / 2):(center[1] + self.init_radius / 2)]
        self.partImg = img
        return img

    def get_part_image_by_size_by_vtk(self, img, center, box_w, box_h, taget_image_w, target_image_h):
        x1 = center[0] - box_w / 2
        x2 = center[0] + box_w / 2
        y1 = center[1] - box_h / 2
        y2 = center[1] + box_h / 2

        if x1 < 0:
            x1 = 0
            x2 = box_w

        if x2 > taget_image_w - 1:
            x1 = taget_image_w - 1 - box_w + 1
            x2 = taget_image_w - 1

        if y1 < 0:
            y1 = 0
            y2 = box_h

        if y2 > target_image_h - 1:
            y1 = target_image_h - 1 - box_h + 1
            y2 = target_image_h - 1

        voi_extractor = vtk.vtkExtractVOI()
        voi_extractor.SetInputData(img)
        voi_extractor.SetVOI(int(x1), int(x2), int(y1), int(y2), 0, 0)
        voi_extractor.Update()

        return ((x1 + x2) / 2, (y1 + y2) / 2), voi_extractor.GetOutput()

    @staticmethod
    def get_part_image_by_size(img, center, radius):
        # adapt local image by radius, boundary exeception
        # print np.shape(input)
        center = np.array(center, dtype=int)
        # print center
        center = np.round(center)

        (l, c) = np.shape(img)

        x1 = int(center[0] - radius // 2)
        x2 = int(center[0] + radius // 2 + 1)
        y1 = int(center[1] - radius // 2)
        y2 = int(center[1] + radius // 2 + 1)

        if x1 < 0:
            x1 = 0
            x2 = radius

        if x2 > c - 1:
            x1 = c - radius
            x2 = c

        if y1 < 0:
            y1 = 0
            y2 = radius

        if y2 > l - 1:
            y1 = l - radius
            y2 = l

        output_img = img[y1:y2, x1:x2]
        return output_img

    def convertt(self, numpy_image):  # convert numpy to vtk
        (row, col) = numpy_image.shape

        image_data = vtk.vtkImageData()
        image_data.SetDimensions(row, col, 1)
        image_data.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)

        for y in range(row):
            for x in range(col):
                image_data.SetScalarComponentFromFloat(y, x, 0, 0, float(numpy_image[x][y]))
        return image_data

    def set_image_to_numpyy(self, input):
        dim = input.GetDimensions()
        flat_v = nps.vtk_to_numpy(input.GetPointData().GetScalars())
        img = flat_v.reshape(dim[0], dim[1], dim[2])
        return img[:, :, 0]

    def set_total_image_to_numpy(self, input):
        dim = input.GetDimensions()
        flat_v = nps.vtk_to_numpy(input.GetPointData().GetScalars())
        img = flat_v.reshape(dim[0], dim[1], dim[2])
        return img

    def numpy_to_vtk(self, input):
        NumPy_data_shape = input.shape
        return nps.numpy_to_vtk(num_array=input.ravel(), deep=True, array_type=vtk.VTK_INT)

    def predict_movement(self, pts):
        point_x = list()
        point_y = list()
        for i in pts:
            point_x.append(i[0])
            point_y.append(i[1])
        mean_point_x = round(np.mean(point_x))
        mean_point_y = round(np.mean(point_y))

        return mean_point_x - 80, mean_point_y - 80

    def removeNoiseKmeansMethod(self, ridge_point, key_point):
        key_point_X = [x for (x, y) in key_point];
        key_point_Y = [y for (x, y) in key_point]
        x = np.array(key_point_X);
        y = np.array(key_point_Y)
        x = x.mean();
        y = y.mean()
        ridge_point = np.array(ridge_point, dtype=float)
        numCluster = 7
        radium = 45
        # print scv.whiten(ridge_point)

        (centroid, label) = scv.kmeans2(ridge_point, numCluster)
        # (centroid, label) = scv.kmeans2(scv.whiten(ridge_point), numCluster)
        pdist = np.linalg.norm(centroid - np.array([x, y]), 2, axis=1)
        indCentroid = np.where(pdist < radium)
        indCentroid = indCentroid[0]
        a = np.array([])

        for i in list(indCentroid):
            a1 = np.where(label == i)

            a = np.concatenate((a, a1[0]))

        r = ridge_point[np.array(a, dtype=int), :]

        return [(x, y) for [x, y] in list(r)]