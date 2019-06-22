#!/usr/bin/env python3
import vtk
import threading

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal, QFileInfo
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import numpy as np
from scipy import signal
from MSADiskImageReader.MSA3DImageReaderInterface import MSA3DImageReaderInterface
from MSADiskImageReader.MSACenterlineTreeReader import MSACenterlineTreeReader


class MSACanvas3D(QFrame):

    volumeDataLoaded = pyqtSignal()

    def __init__(self, parent=None, controller=None, ihm_factor=1, width=0, height=0, background_color="", global_font_color="", global_font=None):
        super(MSACanvas3D, self).__init__()
        self.parent = parent
        self.controller = controller
        self.ihm_factor = ihm_factor
        self.width = width
        self.height = height
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.magnifyFactorWidth = int(self.width * 1.0 )
        self.magnifyFactorHeight = int(self.height * 1.0 )
        self.shrinkFactorWidth = int(1)
        self.shrinkFactorHeight = int(1)

        self.branch_actors = []

        self.textActor = None

        v = self.globalBackgroundColor.split('(')[1].split(')')[0].split(',')

        self.setFixedSize(self.width, self.height)
        self.metadata = {}
        self.current_volume_path = ''
        self.current_volume = None

        self.canvas3D = QVTKRenderWindowInteractor(self)
        self.canvas3D.setFixedSize(self.width, self.height)
        self.ren = vtk.vtkRenderer()
        self.canvas3D.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.canvas3D.GetRenderWindow().GetInteractor()
        self.ren.SetBackground(float(v[0]) / 255, float(v[1]) / 255, float(v[2]) / 255)

        self.volumeDataLoaded.connect(self.do_display_volume_data)
        self.update()

        self.canvas3D.AddObserver("MouseMoveEvent", self.vtk_mouse_move_event)
        self.generate_text_actor()
        self.generate_text_actor_right()

    def generate_text_actor_right(self):
        self.textActor_right = vtk.vtkTextActor()
        self.textActor_right.SetDisplayPosition(30*self.ihm_factor, 60)
        self.textActor_right.GetTextProperty().SetFontSize(15*self.ihm_factor)
        self.textActor_right.GetTextProperty().SetColor(1.0, 1.0, 1.0)
        self.ren.AddActor2D(self.textActor_right)

    def generate_text_actor(self):
        self.textActor = vtk.vtkTextActor()
        self.textActor.SetDisplayPosition(1000*self.ihm_factor, 60)
        self.textActor.GetTextProperty().SetFontSize(15*self.ihm_factor)
        self.textActor.GetTextProperty().SetColor(1.0, 1.0, 1.0)
        self.ren.AddActor2D(self.textActor)

    def vtk_mouse_move_event(self, obj, even):
        pos = self.iren.GetEventPosition()
        x, y = pos
        x = int(round(x / (self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth)))
        y = int(round(y / (self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight)))
        pos_str = 'position:' + '(' + str(x) + ',' + str(y) + ') \n'

        pos_str += 'maximal_grayscale: ' '\n' \
                  + 'minimal_grayscale: ' '\n' \
                   + 'standard_deviation:' '\n' \
                   + 'mean:'

        pos_str_right = 'Image_size: ' '\n' \
                   + 'column: ' '\n' \
                   + 'row:' '\n' \
                   + 'ww:' '\n' \
                   + 'wh:'

        self.textActor.SetInput(pos_str)
        self.textActor_right.SetInput(pos_str_right)
        self.update()

    def read_centerline_by_path(self, center_line_path):
        self.clear()
        print ("read_centerline_by_path", center_line_path)
        centerline_info = QFileInfo(center_line_path)

        if centerline_info.isFile():
            txt_reader = MSACenterlineTreeReader()
            current_centerline = txt_reader.do_read_center_line_tree(center_line_path)

            for branches in range(current_centerline.get_branch_count()):
                if current_centerline.check_centerline_branches(branches):
                    print (len(current_centerline.find_branch_by_index(branches).get_branch_points()))

                    branch_actor = self.do_visualise_vessel_branch(str(branches),
                                                                   current_centerline.find_branch_by_index(branches).get_branch_points(),
                                                                   QColor(0, 200, 0),
                                                                   QColor(0, 100, 0),
                                                                   1)

                    self.branch_actors.append(branch_actor)
                    self.ren.AddActor(branch_actor)

        self.update()

    def do_visualise_vessel_branch(self, name, vessel_points, color1, color2, pts_size):
        centerline_points = vtk.vtkPoints()
        lines = vtk.vtkCellArray()
        poly_data = vtk.vtkPolyData()
        colors = vtk.vtkUnsignedCharArray()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()

        print (len(vessel_points), type(vessel_points), type(vessel_points[0]))
        cpt = 0
        for pts in vessel_points:
            print(pts.get_abscissa(), pts.get_ordinate())
            centerline_points.InsertPoint(cpt, pts.get_abscissa(), pts.get_ordinate(), pts.get_isometric())
            cpt += 1


        lines.InsertNextCell(len(vessel_points))

        for i in range(len(vessel_points)):
            lines.InsertCellPoint(i)

        poly_data.SetPoints(centerline_points)
        poly_data.SetLines(lines)

        colors.SetName(name)
        colors.SetNumberOfComponents(3)
        colors.SetNumberOfTuples(len(vessel_points))

        red_range = color2.red() - color1.red()
        green_range = color2.green() - color1.green()
        blue_range = color2.blue() - color1.blue()
        print("...")
        interval = len(vessel_points)
        for j in range(len(vessel_points)):
            r = 0
            g = 0
            b = 0

            if red_range == 0:
                r = 0
            else:
                r = color1.red() + 1.0 * red_range * j / interval

            if green_range == 0:
                g = 0
            else:
                g = color1.green() + 1.0 * green_range * j / interval

            if blue_range == 0:
                b = 0
            else:
                b = color1.blue() + 1.0 * blue_range * j / interval

            colors.InsertTuple3(j, int(r), int(g), int(b))

        poly_data.GetPointData().AddArray(colors)

        mapper.SetInputData(poly_data)
        mapper.ScalarVisibilityOn()
        mapper.SetScalarModeToUsePointFieldData()
        mapper.SelectColorArray(name)

        actor.SetMapper(mapper)

        return actor

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.setFixedSize(self.width, self.height)
        self.canvas3D.setFixedSize(self.width, self.height)

    def do_display_stl_file(self, file_path):
        stl_reader = vtk.vtkSTLReader()
        stl_reader.SetFileName(file_path)
        stl_reader.Update()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()

        mapper.SetInputConnection(stl_reader.GetOutputPort())
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(150.0 / 255, 150.0 / 255, 150.0 / 255)
        actor.GetProperty().SetOpacity(0.8)
        actor.GetProperty().SetRepresentationToSurface()

        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        self.update()

    def do_find_extreme_points(self, grayscale, frequency):
        ret = []

        for i in range(2, len(grayscale) - 2):
            frequency[i] = (frequency[i - 2] + frequency[i - 1] + frequency[i] + frequency[i + 1] + frequency[i + 2]) // 5

        for i in range(4, len(grayscale) - 4):
            if ((frequency[i] - frequency[i - 1]) * (frequency[i + 1] - frequency[i]) < 0) & ((frequency[i] - frequency[i - 2]) * (frequency[i + 2] - frequency[i]) < 0):
                ret.append((grayscale[i], frequency[i]))
            print('grayscale[i]', i, grayscale[i], 'frequency[i]', frequency[i])
        print('len(ret)', len(ret))

        return ret

    # fileObject = open('/Users/vincent/Desktop/half_body.csv', 'w')
    # for i in range(len(frequency)):
    #     fileObject.write(str(grayscales[i]) + ";" + str(frequency[i]) + '\n')
    # fileObject.close()

    def threshold_seg(self, input, lsb, msb):
        dims = input.GetDimensions()
        for x in range(dims[0]):
            for y in range(dims[1]):
                for z in range(dims[2]):
                    v = input.GetScalarComponentAsFloat(x, y, z, 0)
                    if lsb < v < msb:
                        input.SetScalarComponentFromFloat(x, y, z, 0, float(1.0))
                    else:
                        input.SetScalarComponentFromFloat(x, y, z, 0, float(0.0))
        return input

    def launch(self):
        threading.Thread(None, self.load_volume_data).start()

    def set_current_volume_path(self, current_volume_path):
        self.current_volume_path = current_volume_path

    def stl_file_reader(self, path, mode, opacity, r, g, b, reduction_factor, number_of_interactions):
        # self.ren.RemoveActor()
        reader = vtk.vtkSTLReader()
        mapper = vtk.vtkPolyDataMapper()
        stl_actor = vtk.vtkActor()
        smooth = vtk.vtkSmoothPolyDataFilter()

        reader.SetFileName(path)
        reader.Update()

        smooth.SetInputConnection(reader.GetOutputPort())
        smooth.SetNumberOfIterations(200)
        smooth.BoundarySmoothingOn()

        self.vessel_poly_data = reader.GetOutput()
        mapper.SetInputConnection(smooth.GetOutputPort())

        stl_actor.SetMapper(mapper)
        stl_actor.GetProperty().SetOpacity(opacity)
        stl_actor.GetProperty().SetColor(r * 1.0 / 255, g * 1.0 / 255, b * 1.0 / 255)

        if not mode:
            stl_actor.GetProperty().SetRepresentationToSurface()
        elif mode:
            stl_actor.GetProperty().SetRepresentationToWriteFrame()

        self.ren.AddActor(stl_actor)
        self.ren.ResetCamera()
        self.update()
        # return stl_actor

    def load_volume_data(self):
        interface = MSA3DImageReaderInterface()
        interface.set_file_path(self.current_volume_path)
        interface.load()

        data = interface.get_output()

        # data = self.threshold_seg(data, 0, 1500)

        spacing = np.array(data.GetSpacing())[::-1]
        self.metadata['spacing'] = spacing

        rang = [0, 0]
        data.GetScalarRange(rang)

        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(data)
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()
        histogram = statistics.GetHistogram()

        range_value = maximal_grayscale - minimal_grayscale
        # print maximal_grayscale, minimal_grayscale

        grayscales = []
        frequency = []

        for i in range(int(range_value)):

            if i == 0:
                continue

            index = int(minimal_grayscale) + i
            grayscales.append(index)
            frequency.append(histogram.GetValue(i))

        frequency_np = np.array(frequency).reshape(int(len(frequency)), )
        peakind_pts = list(signal.find_peaks_cwt(frequency_np, np.arange(1, 100)))

        #
        peakind_pts_new = list()
        c = 0
        for pt in peakind_pts:
            if frequency[pt] > 1000:
                peakind_pts_new.append(pt)
            c += 1

        self.parent.plottingBoard.plot(grayscales, frequency)

        # do save histogram
        # print peakind_pts_new
        # fileObject = open('/Users/vincent/Desktop/fr2.csv', 'w')
        # for i in range(len(frequency)):
        #     fileObject.write(str(frequency[i]) + '\n')
        # fileObject.close()

        """
        opacity_transfer_function = vtk.vtkPiecewiseFunction()  # phantom CT
        opacity_transfer_function.AddPoint(minimal_grayscale, 0, 0.5, 0)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.13 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.1732 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.209 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.233 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.25 * range_value, 0.0, 0.49, 0.61)  # box
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.31 * range_value, 0.2, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.342 * range_value, 0.2, 0.49, 0.61)  # 0.2
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.349 * range_value, 0.2, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.354 * range_value, 0.2, 0.49, 0.61)  # 0.2
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.40 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.46 * range_value, 1, 0.49, 0.61)
        opacity_transfer_function.AddPoint(maximal_grayscale, 1.0, 0.5, 0.0)
        """
        # opacity_transfer_function = vtk.vtkPiecewiseFunction()  # CT chest
        # opacity_transfer_function.AddPoint(minimal_grayscale, 0, 0.5, 0)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.02 * range_value, 0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.05 * range_value, 0.0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.08 * range_value, 0.0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.1 * range_value, 0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.20 * range_value, 0.0, 0.33, 0.45)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.30 * range_value, 0.0, 0.33, 0.45)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.370 * range_value, 0.0, 0.33, 0.45)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.375 * range_value, 0.1, 0.33, 0.45)  # lungs appear
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.403 * range_value, 0.0, 0.33, 0.45)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.446 * range_value, 0.1, 0.33, 0.45)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.484 * range_value, 0.0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.497 * range_value, 0.001, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.64 * range_value, 0.2, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.65 * range_value, 0.0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.8 * range_value, 0.0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.90 * range_value, 0.0, 0.49, 0.61)

        opacity_transfer_function = vtk.vtkPiecewiseFunction() # sequence 18
        opacity_transfer_function.AddPoint(minimal_grayscale, 0, 0.5, 0)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.02 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.207 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.222 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.2446 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.2639 * range_value, 0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.29588 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.2959 * range_value, 1, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.075 * range_value, 0.5, 0.49, 0.61)  #contour
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.102 * range_value, 0.5, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.16 * range_value, 0.5, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.226 * range_value, 0.5, 0.49, 0.61)  #
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.365 * range_value, 0.5, 0.33, 0.45)  #
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.46 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(maximal_grayscale, 0, 0.5, 0.0)

        # opacity_transfer_function = vtk.vtkPiecewiseFunction() # sequence 19
        # opacity_transfer_function.AddPoint(minimal_grayscale, 0, 0.5, 0)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.144 * range_value, 0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.223 * range_value, 0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.244 * range_value, 0, 0.49, 0.61)
        # # opacity_transfer_function.AddPoint(minimal_grayscale + 0.265 * range_value, 0, 0.49, 0.61)
        # # opacity_transfer_function.AddPoint(minimal_grayscale + 0.29588 * range_value, 0, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(minimal_grayscale + 0.3066 * range_value, 1, 0.49, 0.61)
        # opacity_transfer_function.AddPoint(maximal_grayscale, 0, 0.5, 0.0)

        """
        opacity_transfer_function = vtk.vtkPiecewiseFunction()  #automatioc half_body
        opacity_transfer_function.AddPoint(minimal_grayscale, 0, 0.5, 0)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.0058 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.068 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.173 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.242 * range_value, 0, 0.33, 0.45)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.265 * range_value, 0, 0.33, 0.45)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.270 * range_value, 0.05, 0.33, 0.45)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.318 * range_value, 0.0, 0.33, 0.45)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.343 * range_value, 0.0, 0.33, 0.45)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.365 * range_value, 0.8, 0.33, 0.45)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.413 * range_value, 0, 0.33, 0.45)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.432 * range_value, 1, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.473 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.494 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.507 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.549 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.589 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.606 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.622 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(minimal_grayscale + 0.995 * range_value, 0, 0.49, 0.61)
        opacity_transfer_function.AddPoint(maximal_grayscale, 0, 0.5, 0.0)
        """
        print ("opacity values:", minimal_grayscale, \
            minimal_grayscale + 0.250 * range_value, \
            minimal_grayscale + 0.310 * range_value, \
            minimal_grayscale + 0.360 * range_value, \
            minimal_grayscale + 0.365 * range_value, \
            minimal_grayscale + 0.46 * range_value, \
            maximal_grayscale)

        # color_transfer_function = vtk.vtkColorTransferFunction()  # CT phantom
        # color_transfer_function.AddRGBPoint(minimal_grayscale, 225.0 / 255, 215.0 / 225.0, 0, 0.5, 1)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.25 * range_value, 1.0, 1.0, 1.0, 0.5, 0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.3098 * range_value, 1, 0.75, 0.75, 0.5, 0)  # new
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.36 * range_value, 1.0, 0.95, 0.95, 0.5, 0.0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.365 * range_value, 1, 1, 1, 0.5, 0.0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.40 * range_value, 230 / 255, 155 / 255, 3 / 255, 0.5, 0.0)
        # color_transfer_function.AddRGBPoint(maximal_grayscale, 230.0 / 255, 155.0 / 225.0, 3.0 / 255, 0.5, 0.0)

        # color_transfer_function = vtk.vtkColorTransferFunction()  # CT chest
        # color_transfer_function.AddRGBPoint(minimal_grayscale, 225.0/255, 215.0/225.0, 0, 0.5, 1)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.10 * range_value, 0.0, 0.0, 255.0/255.0, 0.5, 0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.25 * range_value, 0.0, 0.0, 255.0/255.0, 0.5, 0)  # new
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.30 * range_value, 250.0/255, 145.0/255, 49/255.0, 0.5, 0.0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.380 * range_value, 0/255, 0.0/255, 255/255, 0.5, 0.0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.403 * range_value, 255.0 / 255, 215.0 / 255, 0 / 255, 0.5, 0.0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.446 * range_value, 225.0 / 255, 200.0 / 255, 0 / 255, 0.5, 0.0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.493 * range_value,  255.0 / 255, 255.0 / 255, 0.0 / 255)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.60 * range_value, 255 / 255, 97 / 255, 0.0 / 255,)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.85 * range_value, 255/255, 210/255, 0.0/255, 0.33, 0.45)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.8675 * range_value, 225/255, 215/225, 0.0/255, 0.5, 0.0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.8676 * range_value, 0.0, 0.0, 255/255, 0.5, 0)
        # color_transfer_function.AddRGBPoint(maximal_grayscale, 1.0, 1.0, 1.0, 0.5, 0.0)

        color_transfer_function = vtk.vtkColorTransferFunction()  # manuel half_body
        color_transfer_function.AddRGBPoint(minimal_grayscale,  0.80, 0.60,0.29, 0.5, 1),
        color_transfer_function.AddRGBPoint(minimal_grayscale + 0.2639 * range_value, 1, 0, 0)
        color_transfer_function.AddRGBPoint(minimal_grayscale + 0.3066 * range_value, 0.80, 0.60,0.29)  # new
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.310 * range_value, 1, 0, 0, 0.5,0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.475 * range_value, 0.73, 0.25, 0.30, 0.45,0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.493 * range_value, 0.88, 0.25, 0.30, 0.49, 0.61)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.536 * range_value, 0.88, 0.60, 0.29, 0.33, 0.45)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.570 * range_value, 1, 0.94, 0.95, 0.5, 0.0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.606 * range_value, 0.9, 0.82, 0.56, 0.5, 0)
        color_transfer_function.AddRGBPoint(maximal_grayscale, 1, 0, 0.0, 0.5, 0.0)

        # color_transfer_function = vtk.vtkColorTransferFunction()
        # color_transfer_function.AddRGBPoint(minimal_grayscale, 1, 0, 0, 0.5, 1)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.265 * range_value, 0, 1, 0, 0.5, 0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.270 * range_value, 0, 1, 0, 0.5, 0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.318 * range_value, 1, 0, 0.0, 0.5, 0.52)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.343 * range_value, 1, 0, 0.0, 0.5, 0.52)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.365 * range_value, 1, 0, 0.0, 0.5, 0.52)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.413 * range_value, 0.55, 25, 0.15, 0.33, 0.45)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.452 * range_value, 1, 1, 1, 0.33, 0.45)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.493 * range_value, 0.88, 0.60, 0.29, 0.49, 0.61)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.536 * range_value, 0.9, 0.82, 0.56, 0.33, 0.45)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.570 * range_value, 1, 0.94, 1, 0.5, 0.0)
        # color_transfer_function.AddRGBPoint(minimal_grayscale + 0.606 * range_value, 0.88, 0.60, 0.29, 0.5, 0)
        # color_transfer_function.AddRGBPoint(maximal_grayscale, 1.0, 0.0, 0.0, 0.5, 0.0)

        # set gradient transfer function
        # gradient_transfer_function = vtk.vtkPiecewiseFunction()
        # gradient_transfer_function.AddPoint(minimal_grayscale, 0.0)
        # gradient_transfer_function.AddPoint(minimal_grayscale + 0.0013 * range_value, 0.2)
        # gradient_transfer_function.AddPoint(minimal_grayscale + 0.9870 * range_value, 0.5)
        # gradient_transfer_function.AddPoint(minimal_grayscale + 0.98725 * range_value, 0.5)
        # gradient_transfer_function.AddPoint(minimal_grayscale + 0.9837 * range_value, 0.5)
        # gradient_transfer_function.AddPoint(maximal_grayscale, 0)

        volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()
        # volume_mapper = vtk.vtkSmartVolumeMapper()
        # volume_mapper.SetBlendModeToMaximumIntensity()
        volume_mapper.SetBlendModeToComposite()
        volume_mapper.SetInputData(data)

        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetColor(color_transfer_function)
        volume_property.SetScalarOpacity(opacity_transfer_function)
        volume_property.ShadeOn()
        volume_property.SetInterpolationTypeToLinear()
        # volume_property.SetGradientOpacity(gradient_transfer_function)

        volume_property.SetAmbient(0)
        volume_property.SetDiffuse(1)
        # volume_property.SetSpecular(0.5)
        # volume_property.SetSpecularPower(20.0)
        # volume_property.SetScalarOpacityUnitDistance(0.7919)

        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)

        self.current_volume = volume
        self.volumeDataLoaded.emit()

    def do_display_volume_data(self):
        self.ren.AddVolume(self.current_volume)
        self.ren.ResetCamera()
        self.iren.Initialize()

    def update(self):
        self.canvas3D.GetRenderWindow().Render()
        self.iren.Initialize()

    def clear(self):
        self.ren.RemoveAllViewProps()
