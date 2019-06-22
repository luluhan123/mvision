from MSAModel.MSAStructure.MSAPoint import MSAPoint
from MSAModel.MSAStructure.MSAPointSet import MSAPointSet
import numpy as np


class PointSet2DFindCluster:
    def __init__(self):
        self.minPointNumberPerCluster = 50
        self.tolerantArea = 10
        self.pointsSet = []
        self.predicted_points = []
        self.limit_x = 512
        self.limit_y = 512
        self.underlying_cluster = []

    def set_area_size(self, limit_x, limit_y):
        self.limit_x = limit_x
        self.limit_y = limit_y

    def get_underlying_cluster(self):
        return self.underlying_cluster

    def set_minimum_point_number_per_cluster(self, v):
        self.minPointNumberPerCluster = v

    def set_tolerant_area(self, v):
        self.tolerantArea = v

    def set_point_set(self, pts):
        self.pointsSet = pts

    def execute(self):
        # print("create a markMatrix to record the location of points")
        mark_matrix = np.zeros([self.limit_x, self.limit_y])
        for item in self.pointsSet:
            # '1' means the point does not be visited
            mark_matrix[item[0]][item[1]] = 1
        # print("record the clusters", len(self.pointsSet))
        underlying_cluster = []
        cpt = 0
        for item in self.pointsSet:
            if mark_matrix[item[0]][item[1]] == 1:
                cluster = MSAPointSet()
                # put the first point into the cluster
                msa_point = MSAPoint(cpt, item[0], item[1])
                cluster.append(msa_point)
                cpt += 1
                final_cluster, mark_matrix = self.find_the_cluster(cluster, item, mark_matrix, self.tolerantArea)
                underlying_cluster.append(final_cluster)
        if len(underlying_cluster) > 0:
            self.underlying_cluster = underlying_cluster

    def find_the_cluster(self, cluster, point, mark_matrix, tolerant_area):
        # record neighbors
        neighbors = MSAPointSet()
        # 2 means the point has been visited
        mark_matrix[point[0]][point[1]] = 2
        for i in range(tolerant_area * (-1), tolerant_area + 1):
            for j in range(tolerant_area * (-1), tolerant_area + 1):
                if i != 0 or j != 0:
                    if 0 < point[0] + i < len(mark_matrix) and 0 < point[1] + j < len(mark_matrix):
                        if mark_matrix[point[0] + i][point[1] + j] == 1:
                            mark_matrix[point[0] + i][point[1] + j] = 2
                            msa_point = MSAPoint(0, point[0] + i, point[1] + j)
                            neighbors.append(msa_point)
                            cluster.append(msa_point)
        if neighbors.get_length() > 0:
            # print(len(tempCluster))
            for i in range(neighbors.get_length()):
                item = [0, 0]
                item[0] = neighbors.get_msapoint(i).get_x()
                item[1] = neighbors.get_msapoint(i).get_y()
                self.find_the_cluster(cluster, item, mark_matrix, tolerant_area)
        return cluster, mark_matrix

    def get_centroid(self, uc):
        pts_predicted = []
        for uc_i in uc:
            if uc_i.get_length() > self.minPointNumberPerCluster:
                data = uc_i.get_data_list()
                pts_predicted.append((int(np.mean(data[:, 0])), int(np.mean(data[:, 1]))))
        return pts_predicted

    def get_centroid_rectangle(self, uc):
        pts_predicted = []
        rectangle = []
        for uc_i in uc:
            if uc_i.get_length() > self.minPointNumberPerCluster:
                data = uc_i.get_data_list()
                pts_predicted.append((int(np.mean(data[:, 0])), int(np.mean(data[:, 1]))))
                length = np.max(data[:, 0]) - np.min(data[:, 0])
                width = np.max(data[:, 1]) - np.min(data[:, 1])
                #rectangle.append((length, width))
                rectangle.append((160, 160))
                print("rectangle", rectangle)
        return pts_predicted, rectangle

