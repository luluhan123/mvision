import numpy as np
import math
import vtk
from sklearn.manifold import LocallyLinearEmbedding
from src.MSAModel.MSAStructure.MSAPoint import MSAPoint


class MSAPointSet:
    def __init__(self):
        self.pointSet = []

    def compute_distance(self, pt0, pt1):
        return math.sqrt((pt1.get_x() - pt0.get_x()) ** 2 + (pt1.get_y() - pt0.get_y()) ** 2)

    def compute_total_distance(self, input_pt, pts):
        t = 0
        for pt in pts:
            t += self.compute_distance(input_pt, pt)
        return t

    def end_point_feature(self, input_pt, pts):
        nearest_point = None

        distances = []
        for pt in pts:
            distances.append(self.compute_distance(input_pt, pt))

        min_distance_index = distances.index(min(distances))
        nearest_point = pts[min_distance_index]
        # TODO start your work here.

    def find_nearest_point(self, input):
        distances = []
        for pt in self.pointSet:
            distances.append(self.compute_distance(input, pt))
        min_distance_index = distances.index(min(distances))
        return [min_distance_index, self.pointSet[min_distance_index], min(distances)]

    def to_numpy(self):
        pts = []
        for pt in self.pointSet:
            pts.append([pt.get_x(), pt.get_y()])
        return np.array(pts)

    def lle_sort(self):
        pts_in_np = self.to_numpy()
        lle = LocallyLinearEmbedding(n_components=1, n_neighbors=10)
        pts_reduced = lle.fit_transform(pts_in_np)
        temp = []
        for i in range(len(self.pointSet)):
            self.pointSet[i].set_lle_weight(pts_reduced[i][0])
            temp.append(pts_reduced[i][0])
        temp.sort()
        new_list = []
        for t in temp:
            for pt in self.pointSet:
                if t == pt.get_weight():
                    new_list.append(pt)
                    self.pointSet.remove(pt)
        self.pointSet = new_list

        # temp = []
        # for pt in self.pointSet[i]:
        #     if



    def sort(self):
        # to find start and end point
        distances = []
        for pt in self.pointSet:
            distances.append(self.compute_total_distance(pt, self.pointSet))

        start_point_index = distances.index(max(distances))

        point_set_sorted = list()
        point_set_sorted.append(self.pointSet[start_point_index])
        self.pointSet.pop(start_point_index)

        length = len(self.pointSet) - 1
        cpt = 0
        for i in range(length):
            v = self.find_nearest_point(point_set_sorted[cpt])
            # if v[2] > 35 and v[0] > int(len(self.pointSet)*0.8):
            #     self.pointSet.pop(v[0])
            #     continue
            point_set_sorted.append(self.pointSet[v[0]])
            cpt += 1
            self.pointSet.pop(v[0])

        self.pointSet = point_set_sorted

    def append(self, pt):
        self.pointSet.append(pt)

    def get_length(self):
        return len(self.pointSet)

    def get_msapoint(self, i):
        return self.pointSet[i]

    def get_point_set(self):
        return self.pointSet

    def get_point_at(self, index):
        return self.pointSet[index]

    def get_data_list(self):
        data = []
        for item in self.pointSet:
            data.append((item.x, item.y))
        data = np.array(data)
        new_data = data
        return new_data

    def b_spline_interpolation(self, resolution):

        points = vtk.vtkPoints()

        # x_spline = vtk.vtkSCurveSpline()
        # y_spline = vtk.vtkSCurveSpline()
        # z_spline = vtk.vtkSCurveSpline()

        spline = vtk.vtkParametricSpline()
        spline_source = vtk.vtkParametricFunctionSource()

        number_of_points = len(self.pointSet)  # .get_length()
        for i in range(number_of_points):
            points.InsertNextPoint(self.pointSet[i].get_x(), self.pointSet[i].get_y(), 0)
        #
        # spline.SetXSpline(x_spline)
        # spline.SetYSpline(y_spline)
        # spline.SetZSpline(z_spline)
        spline.SetPoints(points)
        spline_source.SetParametricFunction(spline)
        spline_source.SetUResolution(resolution)
        spline_source.SetVResolution(resolution)
        spline_source.SetWResolution(resolution)
        spline_source.Update()

        pts_nbr = spline_source.GetOutput().GetNumberOfPoints()
        pts_in_vtk = spline_source.GetOutput()

        ret = []

        for i in range(pts_nbr):
            pt = MSAPoint(0, round(pts_in_vtk.GetPoint(i)[0], 2), round(pts_in_vtk.GetPoint(i)[1], 2))
            ret.append(pt)

        #self.pointSet = ret

        return ret

    def interpolation(self, number):
        if number > 1:
            step = len(self.pointSet) // (number - 1)
            list_new = list()
            for i in range(number - 1):
                list_new.append(self.pointSet[i * step])
            list_new.append(self.pointSet[-1])
            self.pointSet = list_new
        return list_new

    def interpolation2(self):
        step = 1
        list_new = list()
        for i in range(len(self.pointSet)):
            list_new.append(self.pointSet[i * step])
        return list_new

    def fit(self, index, ref, reference, patch, radius, number):

        step = 1#len(self.pointSet) // (number - 1)
        list_new = list()
        for i in range(len(self.pointSet) - 1):
            list_new.append(self.pointSet[i * step])
        list_new.append(self.pointSet[-1])

        # snap_list = []
        # for item in list_new:
        #     distance = radius * radius
        #     temp = item
        #     for point in reference:
        #         dis = math.pow(item[0] - point[0], 2) + math.pow(item[1] - point[1], 2)
        #         if dis <= distance:
        #             temp = point
        #             distance = dis
        #     snap_list.append(temp)

        """
        info = ''
        for pt in snap_list:
            info += "before" + "(" + self.color[index] + ':' + str(
                pt[0] - self.global_tacking_area_radius + ref[0]) + ',' + str(
                pt[1] - self.global_tacking_area_radius + ref[1]) + ',' + str(patch[pt[0], pt[1]]) + ");"
        print(info)

        cpt = 0
        for pt in snap_list:
            cpt += patch[pt[0], pt[1]]
        average = int(cpt/len(snap_list))
        tolerant = 5
        result = []
        for pt in snap_list:
            if patch[pt[0], pt[1]] < average - tolerant:
                result.append(self.find_grayscale_peak(pt, patch, 15))
            else:
                result.append(pt)

        info = ''
        for pt in result:
            info += "after"+"(" + self.color[index] + ':' + str(pt[0] - self.global_tacking_area_radius + ref[0]) + ',' + str(pt[1] - self.global_tacking_area_radius + ref[1]) + ',' + str(patch[pt[0], pt[1]]) + ");"
        print(info)
        """
        return list_new
