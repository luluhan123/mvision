#!/usr/bin/env python

import sys
import vtk
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class ProcessWindow(QFrame):
    def __init__(self, parent=None, controller=None, width=0, height=0, target_image_width=0, target_image_height=0, background_color="", global_font_color="", global_font=None):
        QFrame.__init__(self)
        self.parent = parent
        self.controller = controller
        self.width = width
        self.height = height
        self.target_image_width = target_image_width
        self.target_image_height = target_image_height
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.display_width = width
        self.display_height = height

        self.centre_x = 0
        self.centre_y = 0
        self.local_img = None
        self.img = None
        self.local_frangi_display_count = 0
        self.current_local_frangi_image = None

        self.analyserMediator = None
        self.my_plotting_index = 0
        self.my_page_index = 0
        self.target_folder = ''

        # viewer area
        self.analyseImage = QVTKRenderWindowInteractor(self)
        self.imageViewerLayout = QVBoxLayout(self)
        self.imageViewerLayout.addWidget(self.analyseImage)
        self.imageViewerLayout.setContentsMargins(0, 0, 0, 0)
        self.imageViewerLayout.setSpacing(0)

        v = self.globalBackgroundColor.split('(')[1].split(')')[0].split(',')

        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(float(v[0]) / 255, float(v[1]) / 255, float(v[2]) / 255)

        self.analyseImage.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.analyseImage.GetRenderWindow().GetInteractor()

        self.textActor = None

        self.raw_reader = vtk.vtkImageReader()
        self.scaleMagnify = vtk.vtkImageMagnify()
        self.shrink = vtk.vtkImageShrink3D()
        self.mapper = vtk.vtkImageMapper()

        self.guide_wire_result = None
        self.current_x_ray_image = None
        self.first_x_ray_image = None
        self.current_tracer_point = None

        self.ready = False
        self.display_count = 0
        self.file_number = 0

        self.xRayImageWidth = 161
        self.xRayImageHeight = 161

        self.globalBoxRadius = 96
        self.globalBoxRadius1 = 0.01
        self.bboxEnabled = 0

        if sys.platform == 'darwin':
            self.magnifyFactorWeight = 2
        else:
            self.magnifyFactorWeight = 1

        self.magnifyFactorWidth = int(self.width/self.target_image_width)*self.magnifyFactorWeight
        self.magnifyFactorHeight = int(self.height/self.target_image_height)*self.magnifyFactorWeight

        self.shrinkFactorWidth = 1
        self.shrinkFactorHeight = 1

        self.box_w = 0
        self.box_h = 0
        self.window = 0
        self.level = 0

        # self.dims = None
        self.imageToBeDisplayed = None
        self.grayscale = list()
        self.frequency = list()
        self.frangiViewEnable = False
        self.mise_a_jour()

    def marked_points_display(self, current_point, point_sequence, width_ratio, height_ratio, pts_size, color):
        points = vtk.vtkPoints()

        for point in point_sequence:
            points.InsertNextPoint(point[0]*width_ratio, point[1]*height_ratio, 0)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)

        glyph_filter = vtk.vtkVertexGlyphFilter()
        glyph_filter.SetInputData(polydata)
        glyph_filter.Update()

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputConnection(glyph_filter.GetOutputPort())
        mapper.Update()

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        # actor.GetProperty().SetColor(0.2, 1, 1)
        actor.GetProperty().SetColor(color[0]*1.0/ 255, color[1]*1.0 / 255, color[2]*1.0 / 255)
        actor.GetProperty().SetPointSize(pts_size)

        self.renderer.AddActor2D(actor)

        cross = self.display_cross_by_coordinates(current_point, width_ratio, height_ratio)

        self.renderer.AddActor2D(cross[0])
        self.renderer.AddActor2D(cross[1])

    def set_global_window_and_level(self, window, level):
        self.window = window
        self.level = level

    def set_global_voi(self, w, h):
        self.window = w
        self.level = h

    def adjust_image_to_window(self):
        # fetch image parameter information
        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(self.imageToBeDisplayed)
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()

        # adapt image to screen
        self.scaleMagnify.SetInputData(self.imageToBeDisplayed)
        self.scaleMagnify.SetMagnificationFactors(self.magnifyFactorWidth, self.magnifyFactorHeight, 1)

        self.shrink.SetInputConnection(self.scaleMagnify.GetOutputPort())
        self.shrink.SetShrinkFactors( self.shrinkFactorWidth, self.shrinkFactorHeight, 1)

        self.mapper.SetInputConnection(self.shrink.GetOutputPort())
        self.window = maximal_grayscale - minimal_grayscale
        self.level = (maximal_grayscale + minimal_grayscale) / 2
        self.mapper.SetColorWindow(self.window)
        self.mapper.SetColorLevel(self.level)

        actor = vtk.vtkActor2D()
        actor.SetMapper(self.mapper)

        return actor

    def adjust_image_to_window_RWW(self, input):
        self.imageToBeDisplayed = input
        dim = input.GetDimensions()

        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(input)
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()

        # adapt image to screen
        self.scaleMagnify.SetInputData(input)
        self.scaleMagnify.SetMagnificationFactors(self.magnifyFactorWidth, self.magnifyFactorHeight, 1)

        self.shrink.SetInputConnection(self.scaleMagnify.GetOutputPort())
        self.shrink.SetShrinkFactors(self.shrinkFactorWidth, self.shrinkFactorHeight, 1)

        self.mapper.SetInputConnection(self.shrink.GetOutputPort())
        self.window = maximal_grayscale - minimal_grayscale
        self.level = (maximal_grayscale + minimal_grayscale) / 2
        self.mapper.SetColorWindow(self.window)
        self.mapper.SetColorLevel(self.level)

        actor = vtk.vtkActor2D()
        actor.SetMapper(self.mapper)

        return actor

    def ridge_point(self, none_zero_index, r, g, b):
        points = vtk.vtkPoints()

        for point in none_zero_index:
            points.InsertNextPoint(point[0] * self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth, point[1] * self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight, 0)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)

        glyph_filter = vtk.vtkVertexGlyphFilter()
        glyph_filter.SetInputData(polydata)
        glyph_filter.Update()

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputConnection(glyph_filter.GetOutputPort())
        mapper.Update()

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        # actor.GetProperty().SetColor(0.2, 1, 1)
        actor.GetProperty().SetColor(r*1.0/255, g*1.0/255, b*1.0/255)
        actor.GetProperty().SetPointSize(2)
        self.renderer.AddActor2D(actor)

    def adjust_image_to_window_RW(self, input):

        mapper = vtk.vtkImageMapper()
        scaleMagnify = vtk.vtkImageMagnify()
        shrink = vtk.vtkImageShrink3D()

        self.imageToBeDisplayed = input
        dim = input.GetDimensions()

        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(input)
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()
        self.window = maximal_grayscale - minimal_grayscale
        self.level = (maximal_grayscale + minimal_grayscale) / 2

        # adapt image to screen
        scaleMagnify.SetInputData(input)
        scaleMagnify.SetMagnificationFactors(self.magnifyFactorWidth, self.magnifyFactorHeight, 1)
        shrink.SetInputConnection(scaleMagnify.GetOutputPort())
        shrink.SetShrinkFactors(self.shrinkFactorWidth, self.shrinkFactorHeight, 1)

        mapper.SetInputConnection(shrink.GetOutputPort())
        mapper.SetColorWindow(self.window)
        mapper.SetColorLevel(self.level)

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)

        return actor

    def adjust_image_to_window_by_color_level(self, input, a, b):
        self.imageToBeDisplayed = input
        dim = input.GetDimensions()

        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(input)
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()

        # adapt image to screen
        self.scaleMagnify.SetInputData(input)
        self.scaleMagnify.SetMagnificationFactors(1, 1, 1)

        self.shrink.SetInputConnection(self.scaleMagnify.GetOutputPort())
        self.shrink.SetShrinkFactors(2, 2, 1)

        self.mapper.SetInputConnection(self.shrink.GetOutputPort())
        self.window = maximal_grayscale - minimal_grayscale
        self.level = (maximal_grayscale + minimal_grayscale) / 2
        self.mapper.SetColorWindow(self.window)
        self.mapper.SetColorLevel(self.level)

        actor = vtk.vtkActor2D()
        actor.SetMapper(self.mapper)

        return actor

    def amplify_image_to_window(self, centre, input, mag_x, mag_y):
        self.imageToBeDisplayed = input
        dim = input.GetDimensions()

        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(input)
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()

        # adapt image to screen
        self.scaleMagnify.SetInputData(input)
        self.scaleMagnify.SetMagnificationFactors(mag_x, mag_y, 1)

        self.mapper.SetInputConnection(self.scaleMagnify.GetOutputPort())

        self.window = maximal_grayscale - minimal_grayscale
        self.level = (maximal_grayscale + minimal_grayscale) / 2

        self.mapper.SetColorWindow(self.window)
        self.mapper.SetColorLevel(self.level)

        actor = vtk.vtkActor2D()
        actor.SetMapper(self.mapper)
        return actor

    def display_rpca_vtk_image(self, input):

        dim = input.GetDimensions()

        self.imageToBeDisplayed = input

        actor_img = self.adjust_image_to_window_RWW(input)

        self.renderer.RemoveAllViewProps()
        self.renderer.AddActor2D(actor_img)
        self.iren.Initialize()

    def display_vtk_image(self, input):
        self.imageToBeDisplayed = input
        actor_img = self.adjust_image_to_window_RW(input)
        self.renderer.AddActor2D(actor_img)
        self.mise_a_jour()

    def display_ground_truth(self, points):
        image_data = vtk.vtkImageData()
        image_data.SetDimensions(512, 512, 1)
        image_data.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)

        for x in range(512):
            for y in range(512):
                    image_data.SetScalarComponentFromFloat(y, x, 0, 0, float(0))

        for p in points:
            image_data.SetScalarComponentFromFloat(p[0], p[1], 0, 0, float(255))

        actor_img = self.adjust_image_to_window_by_color_level(image_data, 30, 91)
        self.renderer.AddActor2D(actor_img)

    def display_image_by_factor(self, centre, input, mag_x, mag_y):
        self.renderer.RemoveAllViewProps()
        dim = input.GetDimensions()
        row = dim[0]
        col = dim[1]

        self.imageToBeDisplayed = input
        actor_img = self.amplify_image_to_window(centre, input, mag_x, mag_y)
        self.renderer.AddActor2D(actor_img)
        self.mise_a_jour()

    @staticmethod
    def display_cross_by_coordinates(centre, width_ratio,  height_ratio):
        center_x, center_y = centre

        # horizontal
        line_horizontal = vtk.vtkLineSource()
        line_horizontal.SetPoint1(center_x*width_ratio - 50, center_y*height_ratio, 0)
        line_horizontal.SetPoint2(center_x*width_ratio + 50, center_y*height_ratio, 0)
        line_horizontal.SetResolution(5)

        line_horizontal_mapper = vtk.vtkPolyDataMapper2D()
        line_horizontal_mapper.SetInputConnection(line_horizontal.GetOutputPort())
        line_horizontal_mapper.Update()

        line_horizontal_actor = vtk.vtkActor2D()
        line_horizontal_actor.SetMapper(line_horizontal_mapper)
        line_horizontal_actor.GetProperty().SetColor(0.0 / 255, 255.0 / 255, 0.0 / 255)

        line_vertical = vtk.vtkLineSource()
        line_vertical.SetPoint1(center_x*width_ratio, center_y*height_ratio - 50, 0)
        line_vertical.SetPoint2(center_x*width_ratio, center_y*height_ratio + 50, 0)
        line_vertical.SetResolution(5)
        line_vertical_mapper = vtk.vtkPolyDataMapper2D()
        line_vertical_mapper.SetInputConnection(line_vertical.GetOutputPort())
        line_vertical_mapper.Update()

        line_vertical_actor = vtk.vtkActor2D()
        line_vertical_actor.SetMapper(line_vertical_mapper)
        line_vertical_actor.GetProperty().SetColor(0.0 / 255, 255.0 / 255, 0.0 / 255)

        return line_horizontal_actor, line_vertical_actor

    @staticmethod
    def display_point_by_coordinates(centre):
        center_x, center_y = centre

        points = vtk.vtkPoints()
        vertice = vtk.vtkCellArray()
        p = [0]
        p[0] = points.InsertNextPoint(center_x, center_y, 0)
        vertice.InsertNextCell(1, p)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        polydata.SetVerts(vertice)

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputData(polydata)
        mapper.Update()

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.0/255, 250.0/255, 0.0/255)
        actor.GetProperty().SetPointSize(3)
        return actor

    def get_point_actor(self, pts, imageWidth, imageHeight, type='small', color=(1, 0.549, 0), PointSize=3):
        if (type == 'small'):
            magnify_factor_width = int(self.width * 0.2 / 100) + 1
            magnify_factor_height = int(self.height * 0.12 / 100) + 1
            shrink_factor_width = int(imageWidth * 1.0 / 100)
            shrink_factor_height = int(imageHeight * 1.0 / 100)
        else:
            magnify_factor_width = int(self.width * 1.0 / 100) + 1
            magnify_factor_height = int(self.height * 0.6 / 100) + 1
            shrink_factor_width = int(imageWidth * 1.0 / 100)
            shrink_factor_height = int(imageHeight * 1.0 / 100)

        points = vtk.vtkPoints()

        for point in pts:
            x = point[0]
            y = point[1]
            pos_x = x * magnify_factor_width * 1.0 / shrink_factor_width
            pos_y = y * magnify_factor_height * 1.0 / shrink_factor_height
            points.InsertNextPoint(pos_x, pos_y, 0)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)

        glyph_filter = vtk.vtkVertexGlyphFilter()
        glyph_filter.SetInputData(polydata)
        glyph_filter.Update()

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputConnection(glyph_filter.GetOutputPort())
        mapper.Update()

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color[0], color[1], color[2])
        actor.GetProperty().SetPointSize(PointSize)

        return actor

    def set_xray_image_size(self):
        self.xRayImageWidth = 240
        self.xRayImageHeight = 240

    def display(self, img):
        self.imageToBeDisplayed = self.convert(img)
        # self.imageToBeDisplayed = input
        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(self.imageToBeDisplayed)
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()
        histogram = statistics.GetHistogram()
        range_value = maximal_grayscale-minimal_grayscale

        cpt = 0
        for i in range(int(range_value)):
            if cpt == 0:
                cpt += 1
                continue

            index = int(minimal_grayscale)+i
            self.grayscale.append(index)
            self.frequency.append(histogram.GetValue(index))

        # self.parent.manipArea.plot(self.grayscale, self.frequency)

        actor = self.adjust_image_to_window()
        self.display_image(actor)
        self.mise_a_jour()

    def displayy(self, input):
        self.imageToBeDisplayed = self.convert(input)
        # self.imageToBeDisplayed = input
        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(self.imageToBeDisplayed)
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()
        histogram = statistics.GetHistogram()
        range_value = maximal_grayscale-minimal_grayscale

        cpt = 0
        for i in xrange(int(range_value)):
            if cpt == 0:
                cpt += 1
                continue

            index = int(minimal_grayscale)+i
            self.grayscale.append(index)
            self.frequency.append(histogram.GetValue(index))

        actor = self.adjust_image_to_window()
        self.display_image(actor)

    def convert(self, numpy_image):
        image_data = vtk.vtkImageData()
        image_data.SetDimensions(self.xRayImageWidth, self.xRayImageHeight, 1)
        image_data.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)

        for x in range(self.xRayImageWidth):
            for y in range(self.xRayImageHeight):
                image_data.SetScalarComponentFromFloat(y, x, 0, 0, float(255*numpy_image[x][y]))

        return image_data

    def display_image(self, actor):
        self.renderer.AddActor2D(actor)

    def update_background_color(self, r, g, b):
        self.renderer.SetBackground(float(r) / 255, float(g) / 255, float(b) / 255)
        self.iren.Initialize()

    def clear(self):
        self.renderer.RemoveAllViewProps()

    def mise_a_jour(self):
        self.analyseImage.GetRenderWindow().Render()
        self.iren.Initialize()
