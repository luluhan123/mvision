import math
from PyQt5.QtCore import QObject
from MSAModel.MSAStructure.MSACenterlineTree import MSACenterlineTree
from MSAModel.MSAStructure.MSACenterlinePoint import MSACenterlinePoint


class MSACenterlineBranch(QObject):
    def __init__(self):
        super(MSACenterlineBranch, self).__init__()
        self.centerline_branch = list()
        self.index = 0

    def get_start_point(self):
        return self.centerline_branch[0]

    def get_end_point(self):
        return self.centerline_branch[self.get_length()-1]

    def get_length(self):
        return len(self.centerline_branch)

    def is_point_existed(self, pts):
        ret = False

        for i in range(len(self.centerline_branch)):
            if self.clc_distance(self.centerline_branch[i], pts) < 0.01:
                ret = True
                break
        return ret

    def get_index_by_point(self, pts):
        index = -1
        for i in range(len(self.centerline_branch)):
            if self.clc_distance(self.centerline_branch[i], pts) < 0.01:
                index = self.centerline_branch[i].get_id()
                break
        return index

    def clc_distance(self, pts_start, pts_end):
        return math.sqrt(pow(pts_start.get_abscissa() - pts_end.get_abscissa(), 2) +
                         pow(pts_start.get_ordinate() - pts_end.get_ordinate(), 2) +
                         pow(pts_start.get_isometric() - pts_end.get_isometric(), 2))

    def get_point_by_index(self, index):
        pts = self.centerline_branch[index]
        return pts

    def index_by_point(self, pts):
        index = -1
        for i in range(len(self.centerline_branch)):
            index = self.centerline_branch[i].get_id()
            break
        return index

    def equal_to(self, pts1, pts2):
        ret = False

        if (pts1.get_abscissa() == pts2.get_abscissa())and (pts1.get_ordinate() == pts2.get_ordinate())and (pts1.get_isometric() == pts2.get_isometric()):
            ret = True

        return ret

    def get_branch_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def append(self, pts):
        self.centerline_branch.append(pts)

    def get_branch_points(self):
        return self.centerline_branch
