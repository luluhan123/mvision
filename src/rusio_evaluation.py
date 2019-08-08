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
            #line = line.translate(None, '\n')
            if line.__contains__(','):
                v = line.split(',')
                gts.append([int(float(v[0])), int(float(v[1]))])
            elif line.__contains__(';'):
                v = line.split(';')
                gts.append([int(float(v[0])), int(float(v[1]))])
            #print ([int(float(v[0])), int(float(v[1]))])
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
    spline_source.SetUResolution(int(number_of_points/resolution))
    spline_source.SetVResolution(int(number_of_points/resolution))
    spline_source.SetWResolution(int(number_of_points/resolution))
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
    for j in range(len(pts)-1):
        curve_length += compute_distance(pts[j], pts[j+1])
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
for i in range(total_number):
    ref_data = interpolation(sort(do_load_2d_array(path + 'mvision/dat/CTSAWorkspace/' + sequence + '/GTS/' + ''.join(["navi" + str(i).rjust(8, '0')]) + '.dat')), 0.2)
    exp_data = do_load_2d_array(path + 'mvision/dat/CTSAWorkspace/'+ sequence +'/result/'+ ''.join(["navi" + str(i).rjust(8, '0')])+'_'+str(possibility)+'.dat')

    ref_data_length = compute_length(ref_data)
    exp_data_length = compute_length(exp_data)
    # print("before ", num_data_length, exp_data_length)

    #if ref_data_length > exp_data_length :
    ref_data = trancate(ref_data, exp_data, 1)
    #else:
    exp_data = trancate(exp_data, ref_data, 1)

    ref_data = interpolation_by_number(ref_data, 50)
    exp_data = interpolation_by_number(exp_data, 50)
    ref_data_length = compute_length(ref_data)
    exp_data_length = compute_length(exp_data)
    #print("after ", num_data_length, exp_data_length)

    # quantify the difference between the two curves using PCM
    pcm = similaritymeasures.pcm(exp_data, ref_data)

    # quantify the difference between the two curves using
    # Discrete Frechet distance
    df = similaritymeasures.frechet_dist(exp_data, ref_data)

    # quantify the difference between the two curves using
    # area between two curves
    area = similaritymeasures.area_between_two_curves(exp_data, ref_data)

    # quantify the difference between the two curves using
    # Curve Length based similarity measure
    cl = similaritymeasures.curve_length_measure(exp_data, ref_data)

    # quantify the difference between the two curves using
    # Dynamic Time Warping distance
    dtw, d = similaritymeasures.dtw(exp_data, ref_data)
    total_df += df
    total_pcm += pcm
    total_cl += cl
    #print(i, pcm, df, area, cl, dtw)

    if df < 3.01:
        cpt+=1

print ("rate:", cpt, "mdf:", total_df/total_number, "mpcm:", total_pcm/total_number, "mcl:", total_cl/total_number)
    #
    # print(df, dtw)
    # plt.figure()
    # plt.plot(exp_data[:, 0], exp_data[:, 1], 'ro')
    # plt.plot(num_data[:, 0], num_data[:, 1], 'yo')
    # plt.show()
