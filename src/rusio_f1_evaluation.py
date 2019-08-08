import numpy as np
import vtk, math
import similaritymeasures
import matplotlib.pyplot as plt


def compute_distance(pt0, pt1):
    return math.sqrt((pt1[0] - pt0[0]) ** 2 + (pt1[1] - pt0[1]) ** 2)


def compute_total_distance(input_pt, pts):
    t = 0
    for pt in pts:
        t += compute_distance(input_pt, pt)
    t = round(t, 4)
    return t


def find_nearest_distance(input, pts):
    distances = []
    for pt in pts:
        distances.append(compute_distance(input, pt))
    return min(distances)


def find_nearest_point(input, pts):
    distances = []
    for pt in pts:
        distances.append(compute_distance(input, pt))
    min_distance_index = distances.index(min(distances))
    return min_distance_index, pts[min_distance_index], min(distances)


def sort(pts):
    # to find start and end point
    distances = []
    for pt in pts:
        distances.append(compute_total_distance(pt, pts))

    start_point_index = distances.index(max(distances))

    point_set_sorted = list()
    point_set_sorted.append(pts[start_point_index])
    pts.pop(start_point_index)

    length = len(pts) - 1
    for i in range(length):
        v = find_nearest_point(point_set_sorted[i], pts)
        point_set_sorted.append(v[1])
        pts.pop(v[0])

    return point_set_sorted


def do_load_2d_array(path):
    gts = []
    file = open(path, 'r')
    try:
        text_lines = file.readlines()
        for line in text_lines:
            # line = line.translate(None, '\n')
            if line.__contains__(','):
                v = line.split(',')
                gts.append([int(float(v[0])), int(float(v[1]))])
            elif line.__contains__(';'):
                v = line.split(';')
                gts.append([int(float(v[0])), int(float(v[1]))])
            # print ([int(float(v[0])), int(float(v[1]))])
    finally:
        file.close()
    return gts


def interpolation(pts, resolution):
    points = vtk.vtkPoints()

    x_spline = vtk.vtkSCurveSpline()
    y_spline = vtk.vtkSCurveSpline()
    z_spline = vtk.vtkSCurveSpline()

    spline = vtk.vtkParametricSpline()
    spline_source = vtk.vtkParametricFunctionSource()

    number_of_points = len(pts)
    for i in range(number_of_points):
        points.InsertNextPoint(pts[i][0], pts[i][1], 0)

    spline.SetXSpline(x_spline)
    spline.SetYSpline(y_spline)
    spline.SetZSpline(z_spline)
    spline.SetPoints(points)
    spline_source.SetParametricFunction(spline)
    spline_source.SetUResolution(int(number_of_points / resolution))
    spline_source.SetVResolution(int(number_of_points / resolution))
    spline_source.SetWResolution(int(number_of_points / resolution))
    spline_source.Update()

    pts_nbr = spline_source.GetOutput().GetNumberOfPoints()
    pts_in_polydata = spline_source.GetOutput()

    ret = []

    for i in range(pts_nbr):
        pt = [pts_in_polydata.GetPoint(i)[0], pts_in_polydata.GetPoint(i)[1]]
        ret.append(pt)

    return np.array(ret)


def interpolation_by_number(pts, count):
    points = vtk.vtkPoints()

    x_spline = vtk.vtkSCurveSpline()
    y_spline = vtk.vtkSCurveSpline()
    z_spline = vtk.vtkSCurveSpline()

    spline = vtk.vtkParametricSpline()
    spline_source = vtk.vtkParametricFunctionSource()

    number_of_points = len(pts)
    for i in range(number_of_points):
        points.InsertNextPoint(pts[i][0], pts[i][1], 0)

    spline.SetXSpline(x_spline)
    spline.SetYSpline(y_spline)
    spline.SetZSpline(z_spline)
    spline.SetPoints(points)
    spline_source.SetParametricFunction(spline)
    spline_source.SetUResolution(count)
    spline_source.SetVResolution(count)
    spline_source.SetWResolution(count)
    spline_source.Update()

    pts_nbr = spline_source.GetOutput().GetNumberOfPoints()
    pts_in_polydata = spline_source.GetOutput()

    ret = []

    for i in range(pts_nbr):
        pt = [pts_in_polydata.GetPoint(i)[0], pts_in_polydata.GetPoint(i)[1]]
        ret.append(pt)

    return np.array(ret)


def compute_length(pts):
    curve_length = 0
    for j in range(len(pts) - 1):
        curve_length += compute_distance(pts[j], pts[j + 1])
    return curve_length


def find_best_point(input, pts):
    distances = []
    for pt in pts:
        distances.append(compute_distance(input, pt))
    min_distance_index = distances.index(min(distances))
    return pts[min_distance_index]


def trancate(input, ref, tol):
    out = []
    for pt in ref:
        out.append(find_best_point(pt, input))
    return np.array(out)


sequence = "sequence11"
path = "/Users/cheng/Dev/pydev/"
possibility = 0
cpt = 0
total_df = 0.0
total_pcm = 0.0
total_cl = 0.0
total_number = 66

total_missing_rate = 0.0
total_false_rate = 0.0

for i in range(total_number):
    ref_data = interpolation_by_number(sort(do_load_2d_array(path + 'mvision/dat/CTSAWorkspace/' + sequence + '/GTS/' + ''.join(["navi" + str(i).rjust(8, '0')]) + '.dat')), 51)
    exp_data = interpolation_by_number(sort(do_load_2d_array(path + 'mvision/dat/CTSAWorkspace/' + sequence + '/result/' + ''.join(["navi" + str(i).rjust(8, '0')]) + '_' + str(possibility) + '.dat')), 51)

    # missing rate:
    missing_cpt = 0
    for pt in ref_data:
        if find_nearest_distance(pt, exp_data) > 3:
            missing_cpt += 1

    missing_rate = missing_cpt / len(ref_data)
    total_missing_rate += missing_rate

    # false rate
    false_cpt = 0
    for pt in exp_data:
        if find_nearest_distance(pt, ref_data) > 3:
            false_cpt += 1

    false_rate = false_cpt / len(exp_data)
    total_false_rate += false_rate

print("average missing rate,", total_missing_rate / total_number)
print("average false rate,", total_false_rate / total_number)
