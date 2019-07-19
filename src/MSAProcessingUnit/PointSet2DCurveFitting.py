#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
MainWindow of the IHM to contain all the graphic component

author: Cheng WANG

last edited: January 2019
"""
import numpy as np
import math
from MSAModel.MSAStructure.MSAPoint import MSAPoint
from MSAModel.MSAStructure.MSAPointSet import MSAPointSet
from MSAProcessingUnit.PointSet2DConvexHull import PointSet2DConvexHull
import skimage.morphology as morphology


class PointSet2DCurveFitting:
    def __init__(self):
        self.minPointNumberPerCluster = 50
        self.predicted_points = []
        self.predicted_lines_points = []
        self.curve_lengths = []
        self.limit_x = 160
        self.limit_y = 160
        self.predict_curve_length = 200

    def set_area_size(self, limit_x, limit_y):
        self.limit_x = limit_x
        self.limit_y = limit_y

    def get_longest_curve(self):
        if len(self.curve_lengths) > 0:
            index = 0
            # print(len(self.predicted_lines_points))
            for k in range(len(self.predicted_lines_points)):
                if self.predicted_lines_points[k].get_length() > self.predicted_lines_points[index].get_length():
                    index = k
            return self.predicted_lines_points[index]
        else:
            return None

    def get_predicted_points(self):
        return self.predicted_points

    def get_predicted_lines_points(self):
        return self.predicted_lines_points

    def set_minimum_point_number_per_cluster(self, v):
        self.minPointNumberPerCluster = v

    def execute(self, underlying_cluster):
        if len(underlying_cluster) > 0:
            predicted_points, predicted_lines_points, curve_lengths = self.filter_underlying_cluster(underlying_cluster)
            self.predicted_points = predicted_points
            self.predicted_lines_points = predicted_lines_points
            self.curve_lengths = curve_lengths

    def filter_underlying_cluster(self, uc):
        pts_predicted = []
        predicted_lines_points = []
        curve_lengths = []
        # print("uc_size", len(uc))
        for uc_i in uc:
            # print("uc_i_size", len(uc_i))
            pts_predicted, predicted_lines_points, curve_lengths = self.create_curve(uc_i, pts_predicted, predicted_lines_points, curve_lengths)

        return pts_predicted, predicted_lines_points, curve_lengths

    def create_curve(self, uc_i, pts_predicted, predicted_lines_points, curve_lengths):
        if uc_i.get_length() > self.minPointNumberPerCluster:
            data = uc_i.get_data_list()
            # print("data = ", data.tolist())
            len_of_data = len(data[:, 0])
            if len_of_data > 2:
                pts_predicted.append((int(np.mean(data[:, 0])), int(np.mean(data[:, 1]))))
                curve = MSAPointSet()
                for index in range(len_of_data):
                    msa_point = MSAPoint(index, int(data[index][0]), int(data[index][1]))
                    curve.append(msa_point)
                curve = self.use_hull_curve_fitting(curve)
                if curve.get_length() > 0:
                    predicted_lines_points.append(curve)
                else:
                    curve = MSAPointSet()
                    for index in range(len_of_data):
                        msa_point = MSAPoint(index, int(data[index][0]), int(data[index][1]))
                        curve.append(msa_point)
                    predicted_lines_points.append(curve)
                # compute curve length
                curve_length = 0
                for j in range(curve.get_length() - 1):
                    curve_length += self.compute_distance((curve.get_msapoint(j).get_x(),
                                                           curve.get_msapoint(j).get_y()),
                                                          (curve.get_msapoint(j+1).get_x(),
                                                           curve.get_msapoint(j+1).get_y()))
                curve_lengths.append(curve_length)
                # print("curve_length", curve_length)
                # print("pts_predicted size:", len(pts_predicted))
                if curve_length < self.predict_curve_length:
                    if len(pts_predicted) > 1:
                        largest_cluster = predicted_lines_points[0]
                        flag = 0
                        k = 0
                        while -1 < k < len(pts_predicted) - 1:
                            if predicted_lines_points[k].get_length() > largest_cluster.get_length():
                                largest_cluster = predicted_lines_points[k]
                                flag = k
                            new_cluster = self.combine_clusters(predicted_lines_points[-1], predicted_lines_points[flag])
                            if new_cluster.get_length() > 0:
                                # print("len(pts_predicted)", len(pts_predicted))
                                pts_predicted.remove(pts_predicted[-1])
                                predicted_lines_points.remove(predicted_lines_points[-1])
                                curve_lengths.remove(curve_lengths[-1])
                                pts_predicted.remove(pts_predicted[flag])
                                predicted_lines_points.remove(predicted_lines_points[flag])
                                curve_lengths.remove(curve_lengths[flag])
                                pts, lines_points, curve_len = self.create_new_curve(new_cluster)
                                pts_predicted.append(pts)
                                predicted_lines_points.append(lines_points)
                                curve_lengths.append(curve_len)
                                k = k - 1
                            k += 1
                elif curve_length > (3 * self.predict_curve_length) and len(pts_predicted) > 1:
                    pts_predicted.remove(pts_predicted[-1])
                    predicted_lines_points.remove(curve)
                    curve_lengths.remove(curve_length)
        return pts_predicted, predicted_lines_points, curve_lengths

    def use_hull_curve_fitting(self, lines_predicted_points, explore_area=6):
        lines_convex_hull = PointSet2DConvexHull()
        lines_convex_hull.set_lines_points_set(lines_predicted_points)
        lines_convex_hull.set_explore_area(explore_area)
        lines_convex_hull.set_area_size(self.limit_x, self.limit_y)
        lines_convex_hull.execute()
        fullhullPoints = lines_convex_hull.create_full_hull_points()
        line = MSAPointSet()
        mask = np.zeros((self.limit_x, self.limit_y))
        for item in fullhullPoints:
            mask[item[0]][item[1]] = 1

        # use convex hull to get the centerline
        ske = morphology.medial_axis(mask)
        cpt = 0
        for i in range(ske.shape[0]):
            for j in range(ske.shape[1]):
                if ske[i][j]:
                    msa_point = MSAPoint(cpt, i, j)
                    line.append(msa_point)
                    cpt += 1
        return line

    def compute_distance(self, pt0, pt1):
        return math.sqrt((pt1[0] - pt0[0])**2 + (pt1[1] - pt0[1])**2)

    def get_mask(self, data):
        mask = np.zeros([self.limit_x, self.limit_y])
        for item in data:
            mask[item[0]][item[1]] = 1
        return mask

    def find_endpoints(self, data, mask):
        endPoint = []
        secondPoint = []
        for item in data:
            count = []
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i != 0 or j != 0:
                        if mask[item[0] + i][item[1] + j] == 1:
                            count.append((i, j))
            if len(count) == 1:
                endPoint.append((item[0], item[1]))
                secondPoint.append((item[0] + count[0][0], item[1] + count[0][1]))
        return endPoint, secondPoint

    def get_cross_angle(self, l1, l2):
        arr_0 = np.array([(l1[1][0] - l1[0][0]), (l1[1][1] - l1[0][1])])
        arr_1 = np.array([(l2[1][0] - l2[0][0]), (l2[1][1] - l2[0][1])])
        cos_value = (float(arr_0.dot(arr_1)) / (np.sqrt(arr_0.dot(arr_0)) * np.sqrt(arr_1.dot(arr_1))))
        return int(np.arccos(cos_value) * (180 / np.pi)/180)

    def combine_clusters(self, curve1, curve2):
        curve1 = curve1.get_data_list()
        curve2 = curve2.get_data_list()
        mask1 = self.get_mask(curve1)
        mask2 = self.get_mask(curve2)
        endPoint1, secondPoint1 = self.find_endpoints(curve1, mask1)
        endPoint2, secondPoint2 = self.find_endpoints(curve2, mask2)
        angle = []
        dis = []
        for i in range(len(endPoint1)):
            l1 = []
            l1.append(endPoint1[i])
            l1.append(secondPoint1[i])
            for j in range(len(endPoint2)):
                l2 = []
                l2.append(endPoint2[j])
                l2.append(secondPoint2[j])
                angle.append(self.get_cross_angle(l1, l2))
                dis.append(self.compute_distance(l1[0], l2[0]))
        cluster = MSAPointSet()
        flag = False
        for i in range(len(angle)):
            if dis[i] < 50 and 0 <= angle[i] <= 45:
                flag = True
        if flag:
            for index in range(len(curve1)):
                msa_point = MSAPoint(index, int(curve1[index][0]), int(curve1[index][1]))
                cluster.append(msa_point)
            for index in range(len(curve2)):
                msa_point = MSAPoint(index, int(curve2[index][0]), int(curve2[index][1]))
                cluster.append(msa_point)
        # print("combine!", len(cluster))
        return cluster

    def create_new_curve(self, new_cluster):
        curve = MSAPointSet()
        data = new_cluster.get_data_list()
        len_of_data = len(data[:, 0])
        for index in range(len_of_data):
            msa_point = MSAPoint(index, int(data[index][0]), int(data[index][1]))
            curve.append(msa_point)
        curve_length = 0
        curve = self.use_hull_curve_fitting(curve)
        for j in range(curve.get_length() - 1):
            curve_length += self.compute_distance((curve.get_msapoint(j).get_x(),
                                                   curve.get_msapoint(j).get_y()),
                                                  (curve.get_msapoint(j + 1).get_x(),
                                                   curve.get_msapoint(j + 1).get_y()))
        return (int(np.mean(data[:, 0])), int(np.mean(data[:, 1]))), curve, curve_length
