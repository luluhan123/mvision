import math
from MSAModel.MSAStructure.MSACenterlinePointGraph import MSACenterlinePointGraph
from MSAModel.MSAStructure.MSACenterlinePoint import MSACenterlinePoint
from PyQt5.QtCore import QObject


class MSACenterlineTree(QObject):
    def __init__(self):
        super(MSACenterlineTree, self).__init__()
        self.centerline_branches = list()
        self.sparsePointsMap = list()
        self.total_graph = MSACenterlinePointGraph()
        self.sparse_graph = MSACenterlinePointGraph()
        self.sparse_points = list()

    def get_branch_count(self):
        return len(self.centerline_branches)

    def find_nearest_point(self, x, y , z, tolerant_area):
        ret = None
        surface_point = MSACenterlinePoint()

        surface_point.set_abscissa(x)
        surface_point.set_ordinate(y)
        surface_point.set_isometric(z)

        nearest_point_id = 0
        nearst_distance = 100
        for i in range(len(self.centerline_branches)):
            for j in self.centerline_branches[i].get_length():
                pts_front = self.centerline_branches[i].get_point_by_index(j)
                if self.calc_distance(surface_point, pts_front) < nearst_distance:
                    nearst_distance = self.calc_distance(surface_point, pts_front)
                    nearest_point_id = pts_front.get_id()

        if nearst_distance < tolerant_area:
            ret = self.get_point_by_id(nearest_point_id)

        return ret

    def calc_distance(self, pts_start, pts_end):
        return math.sqrt(pow(pts_start.get_abscissa() - pts_end.get_abscissa(), 2) +
                         pow(pts_start.get_ordinate() - pts_end.get_ordinate(), 2) +
                         pow(pts_start.get_isometric() - pts_end.get_isometric(), 2))

    def get_point_by_id(self, index):
        ret = None
        for i in range(len(self.centerline_branches)):
            for j in self.centerline_branches[i].get_length():
                if self.centerline_branches[i].get_point_by_index().get_id() == index:
                    ret = self.centerline_branches[i].get_point_by_index
                    break
        return ret

    def equal_to(self, pts1, pts2):
        ret = False
        if ((pts1.get_abscissa() == pts2.getabscissa())and(pts1.get_ordinate()==pts2.get_ordinate())and(pts1.get_isometric()==pts2.get_isometric())):
            ret = True
        return ret

    def is_point_existed(self, pts):
        ret = False
        for i in range(len(self.centerline_branches)):
            if self.centerline_branches[i].is_point_existed(pts):
                ret = True
                break
        return ret

    def get_index_by_points(self, pts):
        index = -1
        for i in range(len(self.centerline_branches)):
            if self.centerline_branches[i].is_point_existed(pts):
                index = self.centerline_branches[i].get_index_by_point(pts)
                break
        return index

    def append(self, branch):
        self.centerline_branches.append(branch)

    def init_total_centerline_point_graph(self, pts_count):
        return self.total_graph.init(pts_count)

    def init_sparse_centerline_point_graph(self, pts_count):
        return self.sparse_graph.init(pts_count)

    def do_fill_total_graph(self):
        for i in range(len(self.centerline_branches)):
            for j in range(self.centerline_branches[i].get_length()-1):
                self.total_graph.set_value(self.centerline_branches[i].get_point_by_index(j).get_id(),
                                           self.centerline_branches[i].get_point_by_index(j+1).get_id(),
                                           True)
                self.total_graph.set_value(self.centerline_branches[i].get_point_by_index(j+1).get_id(),
                                           self.centerline_branches[i].get_point_by_index(j).get_id(),
                                           True)

    def do_fill_sparse_graph(self):
        for i in range(len(self.centerline_branches)):
            self.sparse_graph.set_value(self.centerline_branches[i].get_start_point().get_sparse_id(),
                                        self.centerline_branches[i].get_end_point().get_sparse_id(),
                                        True)

            self.sparse_graph.set_value(self.centerline_branches[i].get_end_point().get_sparse_id(),
                                        self.centerline_branches[i].get_start_point().get_sparse_id(),
                                        True)

        #self.sparse_graph.print()

    def get_sparse_point_by_index(self, pt):
        ret = -1
        for i in range(len(self.sparse_points)):
            if self.calc_distance(self.sparse_points[i], pt) < 0.001:
                ret = self.sparse_points[i].get_sparse_id()
                break
        return ret

    def is_sparse_point_existed(self, pt):
        ret = False
        for i in range(len(self.sparse_points)):
            if self.calc_distance(self.sparse_points[i], pt) < 0.001:
                ret = True
                break

        return ret

    def set_sparse_point(self):
        count = 0
        for i in range(len(self.centerline_branches)):
            if self.is_sparse_point_existed(self.centerline_branches[i].get_start_point()):
                self.centerline_branches[i].get_start_point().set_sparse_id(self.get_sparse_point_by_index(self.centerline_branches[i].get_start_point()))
            else:
                self.sparse_points.append(self.centerline_branches[i].get_start_point())
                self.sparsePointsMap.append(self.centerline_branches[i].get_start_point().get_id())
                self.centerline_branches[i].get_start_point().set_sparse_id(count)
                self.sparse_points[len(self.sparse_points)-1].set_sparse_id(count)
                count += 1

            if self.is_sparse_point_existed(self.centerline_branches[i].get_end_point()):
                self.centerline_branches[i].get_end_point().set_sparse_id(self.get_sparse_point_by_index(self.centerline_branches[i].get_end_point()))
            else:
                self.sparse_points.append(self.centerline_branches[i].get_end_point())
                self.sparsePointsMap.append(self.centerline_branches[i].get_end_point().get_id())
                self.centerline_branches[i].get_start_point().set_sparse_id(count)
                self.sparse_points[len(self.sparse_points) - 1].set_sparse_id(count)
                count += 1

        return count

    def check_centerline_branches(self, index):

        pts_front = self.find_branch_by_index(index).get_point_by_index(0)
        pts_back = self.find_branch_by_index(index).get_point_by_index(-1)

        print ("pts id",pts_front.get_id(), pts_back.get_id())

        pts_front_cross = self.total_graph.do_check_graph_by_line(pts_front.get_id())
        pts_back_cross = self.total_graph.do_check_graph_by_line(pts_back.get_id())

        print("check result", pts_front_cross, pts_back_cross)

        if (pts_front_cross >1) or (pts_back_cross > 1):
            return True

        return False

    def find_branch_by_index(self, index):
        return self.centerline_branches[index]









