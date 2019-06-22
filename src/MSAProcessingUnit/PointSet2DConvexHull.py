import numpy as np
import math
from MSAModel.MSAStructure.MSAPointSet import MSAPointSet


class PointSet2DConvexHull:
    def __init__(self):
        self.linesPointsSet = MSAPointSet()
        self.valueMatrix = []
        self.exploreArea = 20
        self.limit_x = 512
        self.limit_y = 512
        self.hullEdgePoints = []
        self.fullhullPoints = []

    def set_area_size(self, limit_x, limit_y):
        self.limit_x = limit_x
        self.limit_y = limit_y

    def set_lines_points_set(self, lines_points_set):
        self.linesPointsSet = lines_points_set

    def set_explore_area(self, explore_area):
        self.exploreArea = explore_area

    def get_value_matrix(self):
        return self.valueMatrix

    def get_hull_edge_points(self):
        return self.hullEdgePoints

    def get_full_hull_points(self):
        return self.fullhullPoints

    def execute(self):
        pts = []
        for i in range(self.linesPointsSet.get_length()):
            pts.append((self.linesPointsSet.get_msapoint(i).get_x(), self.linesPointsSet.get_msapoint(i).get_y()))
        self.valueMatrix = self.create_circle(pts)

    def compute_distance(self, pt0, pt1):
        return math.sqrt((pt1[0] - pt0[0]) ** 2 + (pt1[1] - pt0[1]) ** 2)

    def create_circle(self, pts):
        pts.sort()
        pts = pts[::2]
        value_matrix = np.zeros([self.limit_x, self.limit_y])
        if len(pts) > 0:
            for index in range(0, len(pts)):
                x1 = int(pts[index][0] - self.exploreArea)
                y1 = int(pts[index][1] - self.exploreArea)
                x2 = int(pts[index][0] + self.exploreArea + 1)
                y2 = int(pts[index][1] + self.exploreArea + 1)
                if 0 <= x1 < self.limit_x and 0 <= y1 < self.limit_y and 0 <= x2 < self.limit_x and 0 <= y2 < self.limit_y:
                    for i in range(x1, x2):
                        for j in range(y1, y2):
                            distance = int(self.compute_distance((pts[index][0], pts[index][1]), (i, j)))
                            if distance == self.exploreArea and value_matrix[i][j] != 1:
                                value_matrix[i][j] = 2
                            if distance < self.exploreArea:
                                value_matrix[i][j] = 1
        return value_matrix

    def create_hull_edge_points(self):
        hull_edge_points = []
        matrix = self.valueMatrix
        for i in range(0, self.limit_x):
            for j in range(0, self.limit_y):
                if matrix[i][j] == 2:
                    hull_edge_points.append((i, j))
        return hull_edge_points

    def create_full_hull_points(self):
        hull = []
        matrix = self.valueMatrix
        for i in range(0, self.limit_x):
            for j in range(0, self.limit_y):
                if matrix[i][j] == 2:
                    hull.append((i, j))
                if matrix[i][j] == 1:
                    hull.append((i, j))
        return hull
