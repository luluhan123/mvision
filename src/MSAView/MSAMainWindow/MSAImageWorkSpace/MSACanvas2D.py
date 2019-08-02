#!/usr/bin/env python
import vtk
import sys
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QTimer, QDataStream, QIODevice, Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import numpy as np
import cv2
import math
from vtk.util import numpy_support as nps
import os

from src.MSAView.MSAMainWindow.IHMTool.ObjectEvent import ObjectEvent


class MSACanvas2D(QFrame):

    newImageSequenceDropped = pyqtSignal(str)

    def __init__(self, parent=None, controller=None, ihm_factor=1, width=0, height=0, target_image_width=0, target_image_height=0, background_color="", global_font_color="", global_font=None):
        super(MSACanvas2D, self).__init__()

        self.parent = parent
        self.controller = controller
        self.ihm_factor = ihm_factor
        self.width = width
        self.height = height

        self.current_points = []

        self.target_image_width = target_image_width
        self.target_image_height = target_image_height

        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.setAcceptDrops(True)

        self.display_width = width
        self.display_height = height

        self.centre_x = 0
        self.centre_y = 0
        self.local_img = None
        self.img = None

        self.analyserMediator = None
        self.my_plotting_index = 0
        self.my_page_index = 0
        self.target_folder = ''
        self.init_point = (470.48631591796874, 449.57568359375)
        self.init_radius = 120

        self.leftButtonPressed = False
        self.middleButtonPressed = False
        self.rightButtonPressed = False

        self.tracerBoxEnable = False
        self.tracerPointsEnable = False
        self.measureDistanceEnable = False
        self.screenShotEnable = False
        self.showGrayEnable = False
        self.showCoordinateEnable = False
        self.imgRotationEnable = False
        self.generateCurveEnable = False
        self.initialPointsSignEnable = False

        self.centers = list()
        self.distance2points = list()
        self.currentImageActor = None
        self.window = 0
        self.level = 0
        self.box_w = 128
        self.box_h = 128

        self.current_box = None
        self.previous_box = None

        self.pts_actors = list()
        self.textActor = None

        self.scaleMagnify = vtk.vtkImageMagnify()
        self.shrink = vtk.vtkImageShrink3D()
        self.mapper = vtk.vtkImageMapper()

        self.guide_wire_result = None
        self.current_x_ray_image = None
        self.first_x_ray_image = None
        self.current_tracer_point = None
        self.front_image = None

        self.ready = False
        self.display_count = 0
        self.file_number = 0

        self.xRayImageWidth = self.target_image_width
        self.xRayImageHeight = self.target_image_height

        self.globalBoxRadius = 80
        self.globalBoxRadius1 = 0.01
        self.bboxEnabled = 0

        if sys.platform == 'darwin':
            self.magnifyFactorWeight = 2
        else:
            self.magnifyFactorWeight = 1

        self.magnifyFactorWidth = int(self.width * 1.0 / self.target_image_width)*self.magnifyFactorWeight
        self.magnifyFactorHeight = int(self.height * 1.0 / self.target_image_height)*self.magnifyFactorWeight

        self.shrinkFactorWidth = int(1)
        self.shrinkFactorHeight = int(1)

        self.previous_x_ray_image = None
        self.previous_filtered_x_ray_image = None
        self.first_filtered_x_ray_image = None
        self.current_filtered_x_ray_image = None

        self.flag = False
        self.display_timer = QTimer()
        self.doGuidewireTracking = False

        self._ActiveButton = Qt.NoButton

        # viewer area
        self.canvas2D = QVTKRenderWindowInteractor(self)
        self.imageViewerLayout = QVBoxLayout(self)
        self.imageViewerLayout.addWidget(self.canvas2D)
        self.imageViewerLayout.setContentsMargins(0, 0, 0, 0)
        self.imageViewerLayout.setSpacing(0)

        v = self.globalBackgroundColor.split('(')[1].split(')')[0].split(',')

        self.renderer = vtk.vtkRenderer()
        self.canvas2D.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.canvas2D.GetRenderWindow().GetInteractor()
        self.renderer.SetBackground(float(v[0]) / 255, float(v[1]) / 255, float(v[2]) / 255)

        self.display_timer.timeout.connect(self.do_display_current_image)

        self.canvas2D.AddObserver("LeftButtonPressEvent", self.vtk_left_button_press_event)
        ObjectEvent(self.canvas2D).MouseReleased.connect(self.vtk_left_button_release_event)
        self.canvas2D.AddObserver("MiddleButtonPressEvent", self.middle_button_press_event)
        self.canvas2D.AddObserver("RightButtonPressEvent", self.right_button_press_event)
        # self.imageInteractor.AddObserver("MouseMoveEvent",           self.vtk_mouse_move_event)
        ObjectEvent(self.canvas2D).mouseMoveEvent.connect(self.vtk_mouse_move_event)
        self.mise_a_jour()

    def update_background_color(self, r, g, b):
        self.renderer.SetBackground(float(r) / 255, float(g) / 255, float(b) / 255)
        self.mise_a_jour()

    def get_current_x_ray_image(self):
        return self.current_x_ray_image

    def do_display_current_image(self):
        self.clear()

        if self.display_count <= self.controller.get_current_sequence_count() - 1:

            # get image from context by index
            self.current_x_ray_image = self.controller.get_image_by_index(self.display_count)

            if self.current_x_ray_image is None:
                self.parent.display_button_clicked()
                self.pause_image_sequence()
                return

            if not self.doGuidewireTracking:
                self.parent.do_plot_histogram(self.current_x_ray_image.get_values())

            self.display_image(self.adjust_image_to_window())

            self.parent.change_slider_value(self.display_count)

            self.current_x_ray_image.set_state_displayed()

            self.mise_a_jour()

            self.display_count += 1

    def do_display_by_index(self, index):
        self.clear()
        self.display_count = index
        self.current_x_ray_image = self.controller.get_image_by_index(self.display_count)

        if self.current_x_ray_image is None:
            self.parent.display_button_clicked()
            self.pause_image_sequence()
            return

        if not self.doGuidewireTracking:
            self.parent.do_plot_histogram(self.current_x_ray_image.get_values())

        self.display_image(self.adjust_image_to_window())

        self.parent.change_slider_value(self.display_count)

        self.controller.set_image_state_by_index(self.display_count)

        self.mise_a_jour()

    def enable_guidewire_tracking(self):
        self.doGuidewireTracking = not self.doGuidewireTracking

    def set_global_voi(self, w, h):
        self.box_w = w
        self.box_h = h

    def vtk_mouse_move_event(self):
        self.renderer.RemoveActor(self.previous_box)
        pos = self.iren.GetEventPosition()
        ihm_center = pos
        img_center = (int(round(ihm_center[0] *self.magnifyFactorWeight/ (self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth))), int(round(ihm_center[1]*self.magnifyFactorWeight / (self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight))))

        # TODO
        if self.showCoordinateEnable:
            pos_str = 'position:' + '('+str(img_center[0]) + ',' + str(img_center[1]) + ') \n'

            total_img = self.current_x_ray_image.get_values()  # get image value in vtk format

            # extract voi
            centre, part_img = self.controller.get_part_image_by_size_by_vtk(total_img, img_center, self.box_w, self.box_h, self.target_image_width, self.target_image_height)

            # display current region
            self.current_box = self.generate_box(centre, self.box_w, self.box_h)
            self.renderer.AddActor2D(self.current_box)

            # extracted image info
            statistics = vtk.vtkImageHistogramStatistics()
            statistics.SetInputData(part_img)
            statistics.GenerateHistogramImageOff()
            statistics.Update()

            maximal_grayscale = statistics.GetMaximum()
            minimal_grayscale = statistics.GetMinimum()
            mean = statistics.GetMean()
            median = statistics.GetMedian()
            standard_deviation = statistics.GetStandardDeviation()

            pos_str += 'maximal_grayscale: ' + str(maximal_grayscale) + '\n'\
                       + 'minimal_grayscale: ' + str(minimal_grayscale) + '\n'\
                       + 'mean:' + str(mean) + '\n' + 'median:' + str(median) + '\n' \
                       + 'standard_deviation:' + str(standard_deviation)

            if self.textActor is not None:
                self.textActor.SetInput(pos_str)
                self.iren.Initialize()

            self.parent.tracking_image_display(centre, part_img, self.magnifyFactorWidth, self.magnifyFactorHeight)
            self.parent.marked_points_display(centre, self.current_x_ray_image.get_guidewire_tip(), False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
            self.marked_points_display(self.current_x_ray_image.get_guidewire_tip(), self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
            self.previous_box = self.current_box

        if self.initialPointsSignEnable:
            if self._ActiveButton == Qt.LeftButton and self.leftButtonPressed:
                pos_str = 'position:' + '(' + str(img_center[0]) + ',' + str(img_center[1]) + ') \n'

                if self.textActor is not None:
                    self.textActor.SetInput(pos_str)
                    self.iren.Initialize()

                total_img = self.current_x_ray_image.get_values()
                centre, part_img = self.controller.get_part_image_by_size_by_vtk(total_img, img_center, self.box_w, self.box_h, self.target_image_width, self.target_image_height)

                self.parent.tracking_image_display(centre, part_img, self.magnifyFactorWidth, self.magnifyFactorHeight)
                if self.current_x_ray_image.ground_truth_existed(0):
                    self.current_x_ray_image.set_ground_truth_point(0, img_center)
                else:
                    self.current_x_ray_image.create_groud_truth_sequence()
                    self.current_x_ray_image.set_ground_truth_point(0, img_center)

                group_truth = self.current_x_ray_image.get_ground_truth()
                cpt = 0
                for pts in group_truth:
                    if cpt == 0:
                        self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
                    elif cpt == 1:
                        self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 255, 0])
                    elif cpt == 2:
                        self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [0, 0, 255])
                    cpt += 1

            elif self._ActiveButton == Qt.MiddleButton and self.middleButtonPressed:
                pos_str = 'position:' + '(' + str(img_center[0]) + ',' + str(img_center[1]) + ') \n'

                if self.textActor is not None:
                    self.textActor.SetInput(pos_str)
                    self.iren.Initialize()

                total_img = self.current_x_ray_image.get_values()
                centre, part_img = self.controller.get_part_image_by_size_by_vtk(total_img, img_center, self.box_w, self.box_h, self.target_image_width, self.target_image_height)

                self.parent.tracking_image_display(centre, part_img, self.magnifyFactorWidth, self.magnifyFactorHeight)
                if self.current_x_ray_image.ground_truth_existed(1):
                    self.current_x_ray_image.set_ground_truth_point(1, img_center)
                else:
                    self.current_x_ray_image.create_groud_truth_sequence()
                    self.current_x_ray_image.set_ground_truth_point(1, img_center)

                group_truth = self.current_x_ray_image.get_ground_truth()
                cpt = 0
                for pts in group_truth:
                    if cpt == 0:
                        self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
                    elif cpt == 1:
                        self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 255, 0])
                    elif cpt == 2:
                        self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [0, 0, 255])
                    cpt += 1

            elif self._ActiveButton == Qt.RightButton and self.rightButtonPressed:
                pos_str = 'position:' + '(' + str(img_center[0]) + ',' + str(img_center[1]) + ') \n'

                if self.textActor is not None:
                    self.textActor.SetInput(pos_str)
                    self.iren.Initialize()

                total_img = self.current_x_ray_image.get_values()
                centre, part_img = self.controller.get_part_image_by_size_by_vtk(total_img, img_center, self.box_w, self.box_h, self.target_image_width, self.target_image_height)

                self.parent.tracking_image_display(centre, part_img, self.magnifyFactorWidth, self.magnifyFactorHeight)
                if self.current_x_ray_image.ground_truth_existed(2):
                    self.current_x_ray_image.set_ground_truth_point(2, img_center)
                else:
                    self.current_x_ray_image.create_groud_truth_sequence()
                    self.current_x_ray_image.set_ground_truth_point(2, img_center)

                group_truth = self.current_x_ray_image.get_ground_truth()
                cpt = 0
                for pts in group_truth:
                    if cpt == 0:
                        self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
                    elif cpt == 1:
                        self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 255, 0])
                    elif cpt == 2:
                        self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [0, 0, 255])
                    cpt += 1

        if self.tracerPointsEnable:
            pos_str = 'position:' + '(' + str(img_center[0]) + ',' + str(img_center[1]) + ') \n'

            if self.textActor is not None:
                self.textActor.SetInput(pos_str)
                self.iren.Initialize()

            total_img = self.current_x_ray_image.get_values()
            centre, part_img = self.controller.get_part_image_by_size_by_vtk(total_img, img_center, self.box_w, self.box_h, self.target_image_width, self.target_image_height)

            self.parent.tracking_image_display(centre, part_img, self.magnifyFactorWidth, self.magnifyFactorHeight)

            ihm_centre = (int(round(centre[0] * (self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth))), int(round(centre[1] * (self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight))))
            group_truth = self.current_x_ray_image.get_ground_truth()
            cpt = 0
            for pts in group_truth:
                if cpt == 0:
                    self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
                elif cpt == 1:
                    self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 255, 0])
                elif cpt == 2:
                    self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [0, 0, 255])
                cpt += 1

        if self.showGrayEnable:

            self.img = self.set_image_to_numpy(self.current_x_ray_image.get_values())
            grayscale = self.img[img_center[0], img_center[1]]

            gray_str = str(img_center[0]) + ',' + str(img_center[1])+' grayscale value:' + str(grayscale)

            if self.textActor is not None:
                self.textActor.SetInput(gray_str)
                self.iren.Initialize()

    def vtk_left_button_release_event(self):
        if self._ActiveButton == Qt.LeftButton:
            self.leftButtonPressed = False
        elif self._ActiveButton == Qt.MiddleButton:
            self.middleButtonPressed = False
        elif self._ActiveButton == Qt.RightButton:
            self.rightButtonPressed = False

    def vtk_left_button_press_event(self, obj, event):
        self._ActiveButton = Qt.LeftButton
        self.leftButtonPressed = True
        self.renderer.RemoveActor(self.previous_box)

        pos = self.iren.GetEventPosition()
        ihm_center = pos
        img_center = (int(round(ihm_center[0] * self.magnifyFactorWeight / (self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth))), int(round(ihm_center[1] * self.magnifyFactorWeight / (self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight))))

        if self.showCoordinateEnable:
            pos_str = 'position:' + '(' + str(img_center[0]) + ',' + str(img_center[1]) + ') \n'

            total_img = self.current_x_ray_image.get_values()  # get image value in vtk format

            # extract voi
            centre, part_img = self.controller.get_part_image_by_size_by_vtk(total_img, img_center, self.box_w, self.box_h, self.target_image_width, self.target_image_height)

            # display current region
            self.current_box = self.generate_box(centre, self.box_w, self.box_h)
            self.renderer.AddActor2D(self.current_box)

            # extracted image info
            statistics = vtk.vtkImageHistogramStatistics()
            statistics.SetInputData(part_img)
            statistics.GenerateHistogramImageOff()
            statistics.Update()

            maximal_grayscale = statistics.GetMaximum()
            minimal_grayscale = statistics.GetMinimum()
            mean = statistics.GetMean()
            median = statistics.GetMedian()
            standard_deviation = statistics.GetStandardDeviation()

            pos_str += 'maximal_grayscale: ' + str(maximal_grayscale) + '\n' \
                       + 'minimal_grayscale: ' + str(minimal_grayscale) + '\n' \
                       + 'mean:' + str(mean) + '\n' + 'median:' + str(median) + '\n' \
                       + 'standard_deviation:' + str(standard_deviation)

            if self.textActor is not None:
                self.textActor.SetInput(pos_str)
                self.iren.Initialize()

            self.parent.tracking_image_display(centre, part_img, self.magnifyFactorWidth, self.magnifyFactorHeight)
            if self._ActiveButton == Qt.LeftButton and self.leftButtonPressed:
                self.current_x_ray_image.set_guidewire_point(centre)

            self.parent.marked_points_display(centre, self.current_x_ray_image.get_guidewire_tip(), False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
            self.marked_points_display(self.current_x_ray_image.get_guidewire_tip(), self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])

            self.previous_box = self.current_box

        if self.tracerBoxEnable:
            self.renderer.RemoveActor(self.previous_box)
            pos_str = 'position:' + '(' + str(img_center[0]) + ',' + str(img_center[1]) + ') \n'
            total_img = self.current_x_ray_image.get_values()
            centre, part_img = self.controller.get_part_image_by_size_by_vtk(total_img, img_center, self.box_w, self.box_h, self.target_image_width, self.target_image_height)
            self.current_box = self.generate_box(centre, self.box_w, self.box_h)
            self.renderer.AddActor2D(self.current_box)
            statistics = vtk.vtkImageHistogramStatistics()
            statistics.SetInputData(part_img)
            statistics.GenerateHistogramImageOff()
            statistics.Update()

            maximal_grayscale = statistics.GetMaximum()
            minimal_grayscale = statistics.GetMinimum()
            mean = statistics.GetMean()
            median = statistics.GetMedian()
            standard_deviation = statistics.GetStandardDeviation()

            pos_str += 'maximal_grayscale: ' + str(maximal_grayscale) + '\n' \
                       + 'minimal_grayscale: ' + str(minimal_grayscale) + '\n' \
                       + 'mean:' + str(mean) + '\n' + 'median:' + str(median) + '\n' \
                       + 'standard_deviation:' + str(standard_deviation)

            if self.textActor is not None:
                self.textActor.SetInput(pos_str)
                self.iren.Initialize()

            self.parent.tracking_image_display(centre, part_img, self.magnifyFactorWidth, self.magnifyFactorHeight)

            self.previous_box = self.current_box
            return

        if self.tracerPointsEnable:
            self.current_x_ray_image.set_ground_truth_point(img_center)

            pos_str = 'position:' + '(' + str(img_center[0]) + ',' + str(img_center[1]) + ')'

            if self.textActor is not None:
                self.textActor.SetInput(pos_str)
                self.iren.Initialize()

            total_img = self.current_x_ray_image.get_values()
            centre, part_img = self.controller.get_part_image_by_size_by_vtk(total_img, img_center, self.box_w, self.box_h, self.target_image_width, self.target_image_height)

            self.parent.tracking_image_display(centre, part_img, self.magnifyFactorWidth, self.magnifyFactorHeight)
            ihm_centre = (int(round(centre[0] * (self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth))), int(round(centre[1] * (self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight))))
            group_truth = self.current_x_ray_image.get_ground_truth()
            cpt = 0
            for pts in group_truth:
                if cpt == 0:
                    self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
                elif cpt == 1:
                    self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 255, 0])
                elif cpt == 2:
                    self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [0, 0, 255])
                cpt += 1

        if self.showGrayEnable:
            self.img = self.set_image_to_numpy(self.current_x_ray_image.get_values())
            grayscale = self.img[img_center[0], img_center[1]]

            gray_str = str(img_center[0]) + ',' + str(img_center[1]) + ' grayscale value:' + str(grayscale)

            if self.textActor is not None:
                self.textActor.SetInput(gray_str)
                self.iren.Initialize()

        if self.measureDistanceEnable:

            position_in_original_img1 = 'position in original img:' + '(' + str(img_center[1]) + ',' + str([1]) + ')'
            if self.textActor is not None:
                self.textActor.SetInput(position_in_original_img1)

            self.distance2points.append(pos)

            if len(self.distance2points) == 2:
                pointx1, pointy1 = self.distance2points[0]
                pointx2, pointy2 = self.distance2points[1]

                dist = math.sqrt(math.fabs(pointx1 - pointx2) ** 2 + math.fabs(pointy1 - pointy2) ** 2)
                distance = 'distance between two points:' + str(dist)

                if self.textActor is not None:
                    self.textActor.SetInput(distance)
                    self.iren.Initialize()

                self.distance2points = []

        if self.imgRotationEnable:
            print('img rotationed')

    def right_button_press_event(self, obj, event):
        self.rightButtonPressed = True
        self._ActiveButton = Qt.RightButton
        pos = self.iren.GetEventPosition()
        ihm_center = pos*self.magnifyFactorWeight
        img_center = (int(round(ihm_center[0] * self.magnifyFactorWeight / (self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth))), int(round(ihm_center[1] * self.magnifyFactorWeight / (self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight))))

        self.current_x_ray_image.remove_point_in_ground_truth(pos)

        if self.showCoordinateEnable:
            pos_str = 'position:' + '(' + str(img_center[0]) + ',' + str(img_center[1]) + ') \n'

            total_img = self.current_x_ray_image.get_values()  # get image value in vtk format

            # extract voi
            centre, part_img = self.controller.get_part_image_by_size_by_vtk(total_img, img_center, self.box_w, self.box_h, self.target_image_width, self.target_image_height)

            # display current region
            self.current_box = self.generate_box(centre, self.box_w, self.box_h)
            self.renderer.AddActor2D(self.current_box)

            # extracted image info
            statistics = vtk.vtkImageHistogramStatistics()
            statistics.SetInputData(part_img)
            statistics.GenerateHistogramImageOff()
            statistics.Update()

            maximal_grayscale = statistics.GetMaximum()
            minimal_grayscale = statistics.GetMinimum()
            mean = statistics.GetMean()
            median = statistics.GetMedian()
            standard_deviation = statistics.GetStandardDeviation()

            pos_str += 'maximal_grayscale: ' + str(maximal_grayscale) + '\n' \
                       + 'minimal_grayscale: ' + str(minimal_grayscale) + '\n' \
                       + 'mean:' + str(mean) + '\n' + 'median:' + str(median) + '\n' \
                       + 'standard_deviation:' + str(standard_deviation)

            if self.textActor is not None:
                self.textActor.SetInput(pos_str)
                self.iren.Initialize()

            self.parent.tracking_image_display(centre, part_img, self.magnifyFactorWidth, self.magnifyFactorHeight)

            if self._ActiveButton == Qt.RightButton and self.rightButtonPressed:
                self.renderer.RemoveActor(self.previous_box)
                self.current_x_ray_image.remove_guidewire_point(centre)

            self.parent.marked_points_display(centre, self.current_x_ray_image.get_guidewire_tip(), False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
            self.marked_points_display(self.current_x_ray_image.get_guidewire_tip(), self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
            # self.current_x_ray_image.print_guidewire_tip()
            self.previous_box = self.current_box

            self.current_points = self.current_x_ray_image.get_guidewire_tip()

        # # display on current image viewer
        # self.clear()
        # self.display_image(self.currentImageActor)
        # group_truth = self.current_x_ray_image.get_ground_truth()
        # cpt = 0
        # for pts in group_truth:
        #     if cpt == 0:
        #         self.marked_points_display(pts, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
        #     elif cpt == 1:
        #         self.marked_points_display(pts, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 255, 0])
        #     elif cpt == 2:
        #         self.marked_points_display(pts, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [0, 0, 255])
        #     cpt += 1
        # self.mise_a_jour()
        """
        total_img = self.current_x_ray_image.get_values()

        centre, part_img = self.controller.get_part_image_by_size_by_vtk(total_img, img_center, self.box_w, self.box_h, self.target_image_width, self.target_image_height)

        self.parent.tracking_image_display(part_img, self.magnifyFactorWidth, self.magnifyFactorHeight)
        group_truth = self.current_x_ray_image.get_ground_truth()
        cpt = 0
        for pts in group_truth:
            if cpt == 0:
                self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 0, 0])
            elif cpt == 1:
                self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [255, 255, 0])
            elif cpt == 2:
                self.parent.marked_points_display(img_center, pts, False, self.magnifyFactorWidth, self.magnifyFactorHeight, 2, [0, 0, 255])
            cpt += 1
        """
    def set_guidewire_point(self, pt):
        self.current_points = pt

    def get_guidewire_tip(self):
        return self.current_points

    def set_global_window_and_level(self, window, level):
        self.window = window
        self.level = level
        print ("set global window/level", self.window, self.level)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Fetch the parameter's name from a drop event
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")

            stream = QDataStream(data, QIODevice.ReadOnly)
            parameter_name = stream.readQString()
            current_path = str(parameter_name)
            self.ready = False
            self.controller.set_current_sequence_path(current_path)
            self.newImageSequenceDropped.emit(current_path)

    def set_image_sequence_loaded(self):
        self.file_number = self.controller.get_files_number()
        self.parent.set_process_slider(self.file_number)
        self.parent.set_process_slider_value(0)
        self.display_count = 0
        self.ready = True
        self.parent.visualise_files()

        self.parent.display_button_clicked()

    # def curve_display(self, pts, color):
    #     points = vtk.vtkPoints2D()
    #     spline = vtk.vtkParametricSpline()
    #     function_source = vtk.vtkParametricFunctionSource()
    #     mapper = vtk.vtkPolyDataMapper2D()
    #     actor = vtk.vtkActor2D()
    #
    #     for pt in pts:
    #         points.InsertNextPoint(pt)
    #     spline.SetPoints(points)
    #     function_source.SetParametricFunction(spline)
    #     function_source.Update()
    #
    #     mapper.SetInputConnection(function_source.GetOutputPort())
    #     actor.SetMapper(mapper)
    #     self.renderer.AddActor2D(actor)

    '''
    points = vtk.vtkPoints()

        x_spline = vtk.vtkSCurveSpline()
        y_spline = vtk.vtkSCurveSpline()
        z_spline = vtk.vtkSCurveSpline()

        spline = vtk.vtkParametricSpline()
        spline_source = vtk.vtkParametricFunctionSource()

        number_of_points = pts.get_length()
        for i in range(number_of_points):
            points.InsertNextPoint(pts.get_point_at(i).get_x(), pts.get_point_at(i).get_y(), 0)

        spline.SetXSpline(x_spline)
        spline.SetYSpline(y_spline)
        spline.SetZSpline(z_spline)
        spline.SetPoints(points)
        spline_source.SetParametricFunction(spline)
        spline_source.SetUResolution(resolution)
        spline_source.SetVResolution(resolution)
        spline_source.SetWResolution(resolution)
        spline_source.Update()
    '''

    def curve_display(self, pts, centre, color):
        points = vtk.vtkPoints()
        x_spline = vtk.vtkSCurveSpline()
        y_spline = vtk.vtkSCurveSpline()
        z_spline = vtk.vtkSCurveSpline()
        spline = vtk.vtkParametricSpline()
        spline_source = vtk.vtkParametricFunctionSource()
        spline_mapper = vtk.vtkPolyDataMapper2D()
        actor = vtk.vtkActor2D()

        number_of_points = len(pts)

        for point in pts:
            points.InsertNextPoint((point.get_x()+centre[0]-80) * self.magnifyFactorWidth, (point.get_y()+centre[1]-80)* self.magnifyFactorHeight, 0)

        spline.SetXSpline(x_spline)
        spline.SetYSpline(y_spline)
        spline.SetZSpline(z_spline)
        spline.SetPoints(points)
        spline_source.SetParametricFunction(spline)
        spline_source.SetUResolution(200)
        spline_source.SetVResolution(200)
        spline_source.SetWResolution(200)
        spline_source.Update()

        spline_mapper.SetInputConnection(spline_source.GetOutputPort())
        actor.SetMapper(spline_mapper)
        actor.GetProperty().SetColor(color[0]/255, color[1]/255, color[2]/255)
        #actor.GetProperty().SetOpacity(0.6)
        # self.pts_actors.append(actor)
        #
        # for act in self.pts_actors:
        #     self.renderer.AddActor2D(act)
        self.renderer.AddActor2D(actor)

    def points_display(self, pts, color, pts_size):
        points = vtk.vtkPoints()
        # key_points = self.current_x_ray_image.get_key_points()

        for point in pts:
            # self.centers.append((point[0]+centre[0], point[1]))
            points.InsertNextPoint(point[0] * self.magnifyFactorWidth, point[1] * self.magnifyFactorHeight, 0)

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
        actor.GetProperty().SetColor(color[0] * 1.0 / 255, color[1] * 1.0 / 255, color[2] * 1.0 / 255)
        actor.GetProperty().SetPointSize(pts_size)

        self.renderer.AddActor2D(actor)

    def guidewire_display(self, pts, color):
        points = vtk.vtkPoints()

        for point in pts:
            points.InsertNextPoint((point[0])*self.magnifyFactorWidth, (point[1])*self.magnifyFactorHeight, 0)

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
        actor.GetProperty().SetColor(color[0]*1.0/255, color[1]*1.0/255, color[2]*1.0/255)
        actor.GetProperty().SetPointSize(3)

        self.renderer.AddActor2D(actor)

    def global_key_points_display(self, pts, centre, color, radius):
        points = vtk.vtkPoints()

        for point in pts:
            points.InsertNextPoint((point[0] - radius+centre[0])*self.magnifyFactorWidth, (point[1] + centre[1]-radius)*self.magnifyFactorHeight, 0)

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
        actor.GetProperty().SetColor(color[0]*1.0/255, color[1]*1.0/255, color[2]*1.0/255)
        actor.GetProperty().SetPointSize(3)

        self.renderer.AddActor2D(actor)

    def tuple_points_display(self, pts, centre, color, radius):
        points = vtk.vtkPoints()
        x = []
        y = []

        for point in pts:
            points.InsertNextPoint((point[0] - radius+centre[0])*self.magnifyFactorWidth, (point[1] + centre[1]-radius)*self.magnifyFactorHeight, 0)

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
        actor.GetProperty().SetColor(color[0]*1.0/255, color[1]*1.0/255, color[2]*1.0/255)
        actor.GetProperty().SetPointSize(1.5)

        self.renderer.AddActor2D(actor)

    def draw_tuple_point_cloud_by_order(self, pts, centre, color, radius):
        for h in pts:
            self.draw_a_single_tuple_point(h, centre, color, radius)

    def draw_a_single_tuple_point(self,  pt, centre, color, radius):
        polygonSource = vtk.vtkRegularPolygonSource()
        # polygonSource.GeneratePolygonOff()
        polygonSource.SetNumberOfSides(50)
        polygonSource.SetRadius(2)
        polygonSource.SetCenter((pt[0] - radius + centre[0]) * self.magnifyFactorWidth, (pt[1] + centre[1] - radius) * self.magnifyFactorHeight, 0)

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputConnection(polygonSource.GetOutputPort())
        mapper.Update()

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color[0] * 1.0 / 255, color[1] * 1.0 / 255, color[2] * 1.0 / 255)
        actor.GetProperty().SetPointSize(1 * self.ihm_factor)
        self.renderer.AddActor2D(actor)

    def draw_point_cloud_by_order(self, pts, centre, color, radius, size):
        for h in pts:
            self.draw_a_single_point(h, centre, (color.red(), color.green(), color.blue()), radius, size)

    def draw_a_single_point(self, pt, centre, color, radius, size):
        polygonSource = vtk.vtkRegularPolygonSource()
        #polygonSource.GeneratePolygonOff()
        polygonSource.SetNumberOfSides(12)
        polygonSource.SetRadius(size)
        polygonSource.SetCenter((pt.get_x() - radius+centre[0])*self.magnifyFactorWidth, (pt.get_y() + centre[1]-radius)*self.magnifyFactorHeight, 0)

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputConnection(polygonSource.GetOutputPort())
        mapper.Update()

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color[0] * 1.0 / 255, color[1] * 1.0 / 255, color[2] * 1.0 / 255)
        actor.GetProperty().SetPointSize(size * self.ihm_factor)
        self.renderer.AddActor2D(actor)

    def contour_key_points_display(self, pts, centre, color, radius):
        points = vtk.vtkPoints()
        x = []
        y = []

        for point in pts:
            points.InsertNextPoint((point[0] - radius+centre[0])*self.magnifyFactorWidth, (point[1] + centre[1]-radius)*self.magnifyFactorHeight, 0)

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
        actor.GetProperty().SetColor(color[0]*1.0/255, color[1]*1.0/255, color[2]*1.0/255)
        actor.GetProperty().SetPointSize(1.5*self.ihm_factor)

        self.renderer.AddActor2D(actor)

    def key_points_display(self, pts, centre, color, radius):
        points = vtk.vtkPoints()
        x = []
        y = []

        for point in pts:
            points.InsertNextPoint((point.get_x() - radius+centre[0])*self.magnifyFactorWidth, (point.get_y() + centre[1]-radius)*self.magnifyFactorHeight, 0)

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
        actor.GetProperty().SetColor(color[0]*1.0/255, color[1]*1.0/255, color[2]*1.0/255)
        actor.GetProperty().SetPointSize(1.5*self.ihm_factor)

        self.renderer.AddActor2D(actor)

    def special_key_points_display(self, pts, centre, color):

        # for point in pts:
        #     (x,y) = point.pt
        #     self.current_x_ray_image.set_key_points(point.pt)

        points = vtk.vtkPoints()
        # key_points = self.current_x_ray_image.get_key_points()

        for point in pts:
            # self.centers.append((point[0]+centre[0], point[1]))
            points.InsertNextPoint((point[0][0]-80+centre[0])*self.magnifyFactorWidth, (point[0][1]+centre[1]-80)*self.magnifyFactorHeight, 0)

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
        actor.GetProperty().SetColor(color[0]*1.0/255, color[1]*1.0/255, color[2]*1.0/255)
        actor.GetProperty().SetPointSize(3)

        self.renderer.AddActor2D(actor)

    def show_coordinate_enable(self, flag):
        self.showCoordinateEnable = flag
        self.tracerBoxEnable = False
        self.tracerPointsEnable = False
        self.measureDistanceEnable = False
        self.screenShotEnable = False
        self.showGrayEnable = False
        self.initialPointsSignEnable = False
        if self.showCoordinateEnable:
            self.setCursor(QCursor(Qt.CrossCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def enable_show_gray(self, flag):
        self.showGrayEnable = flag
        self.tracerBoxEnable = False
        self.tracerPointsEnable = False
        self.measureDistanceEnable = False
        self.screenShotEnable = False
        self.showCoordinateEnable = False
        self.initialPointsSignEnable = False
        if self.showGrayEnable:
            self.setCursor(QCursor(Qt.CrossCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def enabled_screen_shot(self, flag):
        self.screenShotEnable = flag
        self.tracerBoxEnable = False
        self.tracerPointsEnable = False
        self.measureDistanceEnable = False
        self.showGrayEnable = False
        self.showCoordinateEnable = False
        self.initialPointsSignEnable = False
        if self.screenShotEnable:
            self.setCursor(QCursor(Qt.CrossCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def enabled_distance_mea(self, flag):
        self.measureDistanceEnable = flag
        self.tracerBoxEnable = False
        self.tracerPointsEnable = False
        self.screenShotEnable = False
        self.showGrayEnable = False
        self.showCoordinateEnable = False
        self.initialPointsSignEnable = False
        if self.measureDistanceEnable:
            self.setCursor(QCursor(Qt.CrossCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def enable_initial_points_sign(self, flag):
        self.initialPointsSignEnable = flag
        self.tracerPointsEnable = False
        self.tracerBoxEnable = False
        self.measureDistanceEnable = False
        self.screenShotEnable = False
        self.showGrayEnable = False
        self.showCoordinateEnable = False

        if self.tracerPointsEnable:
            self.setCursor(QCursor(Qt.CrossCursor))
            # self.current_x_ray_image.find_ground_truth_existed()
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))
            # self.current_x_ray_image.save_ground_truth()

        # if not self.initialPointsSignEnable:
        #     initial_pts = self.current_x_ray_image.get_ground_truth()
        #
        #     # initial_img = np.zeros([self.target_image_width, self.target_image_height])
        #
        #     ground_truth_initial_point = list()
        #     background_initial_point = list()
        #
        #     cpt = 0
        #     for pts in initial_pts:
        #         if cpt == 0:
        #             ground_truth_initial_point = pts
        #         elif cpt == 1:
        #             background_initial_point = pts
        #         cpt += 1
        #
        #     print(ground_truth_initial_point)
        #
        #     print(background_initial_point)
        #
        #     total_img = self.controller.set_image_to_numpy(self.current_x_ray_image.get_values())
        #
        #     gc = GraphCut()
        #     gc.set_input_img(total_img)
        #     gc.set_background_point_set(background_initial_point)
        #     gc.set_ground_truth_point_set(ground_truth_initial_point)
        #     ret = gc.execute()

    def enabled_tracer_points(self, flag):
        self.tracerPointsEnable = flag
        self.tracerBoxEnable = False
        self.measureDistanceEnable = False
        self.screenShotEnable = False
        self.showGrayEnable = False
        self.showCoordinateEnable = False
        self.initialPointsSignEnable = False
        if self.tracerPointsEnable:
            self.setCursor(QCursor(Qt.CrossCursor))
            # self.current_x_ray_image.find_ground_truth_existed()
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))
            # self.current_x_ray_image.save_ground_truth()

    def enable_box_tracer(self, flag):
        self.tracerBoxEnable = flag
        self.tracerPointsEnable = False
        self.measureDistanceEnable = False
        self.screenShotEnable = False
        self.showGrayEnable = False
        self.showCoordinateEnable = False
        self.initialPointsSignEnable = False
        if self.tracerBoxEnable:
            self.setCursor(QCursor(Qt.CrossCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def enable_img_rotation(self, flag):
        self.imgRotationEnable = flag
        self.tracerBoxEnable = False
        self.tracerPointsEnable = False
        self.measureDistanceEnable = False
        self.screenShotEnable = False
        self.showGrayEnable = False
        self.showCoordinateEnable = False
        self.initialPointsSignEnable = False
        if self.imgRotationEnable:
            self.setCursor(QCursor(Qt.CrossCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def enable_generate_curve(self, flag):
        self.generateCurveEnable = flag
        self.tracerBoxEnable = False
        self.tracerPointsEnable = False
        self.measureDistanceEnable = False
        self.screenShotEnable = False
        self.showGrayEnable = False
        self.showCoordinateEnable = False
        self.imgRotationEnable = False
        self.initialPointsSignEnable = False
        if self.generateCurveEnable:
            self.setCursor(QCursor(Qt.CrossCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def middle_button_press_event(self, obj, event):
        self._ActiveButton = Qt.MiddleButton
        self.middleButtonPressed = True
        return

    def marked_points_display(self, point_sequence,  width_ratio, height_ratio, pts_size, color):
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
        actor.GetProperty().SetColor(color[0]*1.0 / 255, color[1]*1.0 / 255, color[2]*1.0 / 255)
        actor.GetProperty().SetPointSize(pts_size)

        self.renderer.AddActor2D(actor)

    def generate_boxing(self, center_x, center_y):

        points = vtk.vtkPoints()

        points.InsertNextPoint(center_x - self.globalBoxRadius, center_y + self.globalBoxRadius, 0)
        points.InsertNextPoint(center_x + self.globalBoxRadius, center_y + self.globalBoxRadius, 0)
        points.InsertNextPoint(center_x + self.globalBoxRadius, center_y - self.globalBoxRadius, 0)
        points.InsertNextPoint(center_x - self.globalBoxRadius, center_y - self.globalBoxRadius, 0)

        lines = vtk.vtkCellArray()
        lines.InsertNextCell(5)
        lines.InsertCellPoint(0)
        lines.InsertCellPoint(1)
        lines.InsertCellPoint(2)
        lines.InsertCellPoint(3)
        lines.InsertCellPoint(0)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        polydata.SetLines(lines)

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputData(polydata)
        mapper.Update()

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.2, 1, 1)
        actor.GetProperty().SetPointSize(50)
        return actor

    def tracked_point(self, centre, color):
        center_x = centre[0]*self.magnifyFactorWidth
        center_y = centre[1]*self.magnifyFactorHeight

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
        actor.GetProperty().SetColor(color[0]*1.0/255, color[1]*1.0/255, color[2]*1.0/255)
        actor.GetProperty().SetPointSize(3)

        self.renderer.AddActor2D(actor)

    def generate_box(self, pos, w, h):
        center_x = pos[0]
        center_y = pos[1]

        points = vtk.vtkPoints()
        vertex = vtk.vtkVertex()

        points.InsertNextPoint((center_x - w/2)*(self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth), (center_y + h/2)*(self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight), 0)
        points.InsertNextPoint((center_x + w/2)*(self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth), (center_y + h/2)*(self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight), 0)
        points.InsertNextPoint((center_x + w/2)*(self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth), (center_y - h/2)*(self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight), 0)
        points.InsertNextPoint((center_x - w/2)*(self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth), (center_y - h/2)*(self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight), 0)

        lines = vtk.vtkCellArray()
        lines.InsertNextCell(5)
        lines.InsertCellPoint(0)
        lines.InsertCellPoint(1)
        lines.InsertCellPoint(2)
        lines.InsertCellPoint(3)
        lines.InsertCellPoint(0)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        polydata.SetLines(lines)

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputData(polydata)
        mapper.Update()

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1.0*255/255, 1.0*255/255, 1.0*51/255)
        actor.GetProperty().SetPointSize(50)

        return actor

    def generate_box_and_display(self, pos, w, h, colors):
        center_x = pos[0]#*self.magnifyFactorWidth
        center_y = pos[1]#*self.magnifyFactorHeight

        points = vtk.vtkPoints()
        vertex = vtk.vtkVertex()

        points.InsertNextPoint(((center_x - w/2)*(self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth), (center_y + h/2)*(self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight), 0))
        points.InsertNextPoint(((center_x + w/2)*(self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth), (center_y + h/2)*(self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight), 0))
        points.InsertNextPoint(((center_x + w/2)*(self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth), (center_y - h/2)*(self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight), 0))
        points.InsertNextPoint(((center_x - w/2)*(self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth), (center_y - h/2)*(self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight), 0))

        lines = vtk.vtkCellArray()
        lines.InsertNextCell(5)
        lines.InsertCellPoint(0)
        lines.InsertCellPoint(1)
        lines.InsertCellPoint(2)
        lines.InsertCellPoint(3)
        lines.InsertCellPoint(0)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        polydata.SetLines(lines)

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputData(polydata)
        mapper.Update()

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1.0*colors[0]/255, 1.0*colors[1]/255, 1.0*colors[2]/255)
        actor.GetProperty().SetPointSize(5)

        self.renderer.AddActor2D(actor)

    def track_point(self, centre):
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
        actor.GetProperty().SetColor(255.0/255, 128.0/255, 0.0/255)
        actor.GetProperty().SetPointSize(1)
        return actor

    def is_ready(self):
        return self.ready

    def display_image_sequence(self):
        self.display_timer.start(10)

    def pause_image_sequence(self):
        self.display_timer.stop()

    @staticmethod
    def do_parse_vessel_file(path):
        # print path
        center_line = []
        f = open(path, 'r')
        # print 'do_parse_vessel_file', f

        for line in f:
            line = line.split(',')
            center_line.append([float(line[0].split(':')[1]), float(line[1].split(':')[1])])
        f.close()
        return center_line

    def enhance_guide_wire(self):
        # print self.current_x_ray_image.get_values()
        return self.controller.enhance_guide_wire(self.current_x_ray_image.get_values())

    def modifier_display_size(self, w, h):
        self.display_width = w
        self.display_height = h

    def restore_display_size(self):
        self.display_width = self.width
        self.display_height = self.height*0.95

    def rescale_image_to_window(self, img):
        # fetch image parameter information
        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(img)
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()

        # adapt image to screen
        self.scaleMagnify.SetInputData(img)
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

    def adjust_image_to_window(self):
        # fetch image parameter information
        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(self.current_x_ray_image.get_values())
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()

        # adapt image to screen
        self.scaleMagnify.SetInputData(self.current_x_ray_image.get_values())
        self.scaleMagnify.SetMagnificationFactors(self.magnifyFactorWidth, self.magnifyFactorHeight, 1)

        self.shrink.SetInputConnection(self.scaleMagnify.GetOutputPort())
        self.shrink.SetShrinkFactors(self.shrinkFactorWidth, self.shrinkFactorHeight, 1)

        self.mapper.SetInputConnection(self.shrink.GetOutputPort())

        self.window = maximal_grayscale - minimal_grayscale
        self.level = (maximal_grayscale + minimal_grayscale)/2

        self.mapper.SetColorWindow(self.window)
        self.mapper.SetColorLevel(self.level)

        actor = vtk.vtkActor2D()
        actor.SetMapper(self.mapper)

        return actor

    def generate_curve(self):
        self.current_x_ray_image.set_filtered_values(
            self.controller.enhance_guide_wire(self.current_x_ray_image.get_values()))

        if self.display_count == 0:
            self.first_x_ray_image = self.controller.get_image_by_index(self.display_count)

            self.first_filtered_x_ray_image = self.first_x_ray_image.get_filteraed_values()
            self.first_filtered_x_ray_image = (1.0 * 255.0 * self.first_filtered_x_ray_image) / np.amax(self.first_filtered_x_ray_image )

            return None

        elif self.display_count > 0:

            initial_win_abs_x = 350
            initial_win_high = 70
            initial_win_abs_y = 230
            initial_win_with = 120

            initialize_track_window = (initial_win_abs_y,
                                       initial_win_abs_x,
                                       initial_win_with,
                                       initial_win_high)

            gray_roi = self.first_filtered_x_ray_image[initial_win_abs_x:initial_win_abs_x+initial_win_high, initial_win_abs_y: initial_win_abs_y+initial_win_with]
            gray_roi = np.uint8(gray_roi)

            mask = cv2.inRange(gray_roi,
                               np.array(1),
                               np.array(255))
            gray_roi_hist = cv2.calcHist([gray_roi], [0], mask, [255], [0, 255])
            cv2.normalize(gray_roi_hist, gray_roi_hist, 0, 3, cv2.NORM_MINMAX)

            termination_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

            self.current_filtered_x_ray_image = self.current_x_ray_image.get_filtered_values()
            self.current_filtered_x_ray_image = (1.0 * 255.0 * self.current_filtered_x_ray_image) / np.amax(self.current_filtered_x_ray_image)
            self.current_filtered_x_ray_image = np.uint8(self.current_filtered_x_ray_image)

            probability_estimation = cv2.calcBackProject([self.current_filtered_x_ray_image],
                                                         [0], gray_roi_hist,
                                                         [0, 255], 1)

            track_window = cv2.meanShift(probability_estimation,
                                         initialize_track_window,
                                         termination_criteria)

            x, y, w, h = track_window[1][0], track_window[1][1], track_window[1][2], track_window[1][3]

            points = vtk.vtkPoints()

            points.InsertNextPoint(x, y, 0)
            points.InsertNextPoint(x, (y+h), 0)
            points.InsertNextPoint((x+w), (y+h), 0)
            points.InsertNextPoint((x+w), y, 0)

            lines = vtk.vtkCellArray()
            lines.InsertNextCell(5)
            lines.InsertCellPoint(0)
            lines.InsertCellPoint(1)
            lines.InsertCellPoint(2)
            lines.InsertCellPoint(3)
            lines.InsertCellPoint(0)

            polydata = vtk.vtkPolyData()
            polydata.SetPoints(points)

            mapper = vtk.vtkPolyDataMapper2D()
            mapper.SetInputData(polydata)
            mapper.Update()

            actor = vtk.vtkActor2D()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(0.2, 1, 1)
            actor.GetProperty().SetPointSize(5)

            return actor

    def generate_text_actor(self):
        self.textActor = vtk.vtkTextActor()
        self.textActor.SetDisplayPosition(10, 10)
        self.textActor.GetTextProperty().SetFontSize(15)
        self.textActor.GetTextProperty().SetColor(1.0, 1.0, 1.0)
        self.renderer.AddActor2D(self.textActor)

    def local_frangi(self):
        self.img = self.set_image_to_numpy(self.current_x_ray_image.get_values())
        r1 = int(int(self.init_point[0]) / (self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth))
        r2 = int(int(self.init_point[1]) / (self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight))

        self.local_img = self.img[r1 - self.init_radius: r1 + self.init_radius, r2 - self.init_radius: r2 + self.init_radius]
        return self.controller.enhance_local_guide_wire(self.local_img)

    def set_image_to_numpy(self, input):
        dim = input.GetDimensions()
        flat_v = nps.vtk_to_numpy(input.GetPointData().GetScalars())
        img = flat_v.reshape(dim[0], dim[1], dim[2])
        img = img[:, :, 0]
        return img

    def do_parse_target(self):
        target = self.target_folder + self.img_prefix + str(self.img_index) + '.txt'
        if os.path.exists(target):
            self.guide_wire_result = self.target_folder + str(self.img_index) + '.txt'

            img_actor = self.adjust_image_to_window()
            self.display_image(img_actor)
            self.img_index += 1

    def ridge_point(self, none_zero_index):
        points = vtk.vtkPoints()

        for point in none_zero_index:
            points.InsertNextPoint(point[1] * self.magnifyFactorWidth * 1.0 / self.shrinkFactorWidth, point[0] * self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight, 0)

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
        actor.GetProperty().SetColor(0.2, 1, 1)
        actor.GetProperty().SetPointSize(3)

        self.renderer.AddActor2D(actor)
        self.iren.Initialize()

    def generate_gvf_points(self):
        # print self.guide_wire_result
        target = ''
        if self.display_count < 10:
            target = self.result_path + '00'+ str(self.display_count)+'.txt'
        elif (self.display_count >= 10) and (self.display_count < 100):
            target = self.result_path + '0' + str(self.display_count)+'.txt'
        elif self.display_count >= 100:
            target = self.result_path + str(self.display_count)+'.txt'

        gw = self.do_parse_vessel_file(target)

        points = vtk.vtkPoints()

        for point in gw:
            points.InsertNextPoint(point[0] * self.magnifyFactorWidth * 1.0 /self.shrinkFactorWidth, (511- point[1]) * self.magnifyFactorHeight * 1.0 / self.shrinkFactorHeight, 0)

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
        actor.GetProperty().SetColor(0.2, 1, 1)
        actor.GetProperty().SetPointSize(3)

        self.renderer.AddActor2D(actor)
        self.iren.Initialize()

    def display_image(self, actor):
        self.currentImageActor = actor
        self.renderer.AddActor2D(actor)
        self.generate_text_actor()

    def mise_a_jour(self):
        self.canvas2D.GetRenderWindow().Render()
        self.iren.Initialize()

    def clear(self):
        self.renderer.RemoveAllViewProps()

    def nettoyer(self):
        self.display_count = 0
        self.current_x_ray_image = None
        self.renderer.RemoveAllViewProps()

    def get_rectangle_and_display(self, center, min_x, max_x, min_y, max_y, tolerant_area, colors):

        points = vtk.vtkPoints()
        points.InsertNextPoint(((min_x - 80 + center[0]) * self.magnifyFactorWidth-tolerant_area,
                                (min_y-80 + center[1]) * self.magnifyFactorWidth-tolerant_area, 0))

        points.InsertNextPoint(((max_x - 80 + center[0]) * self.magnifyFactorWidth + tolerant_area,
                                (min_y - 80 + center[1]) * self.magnifyFactorWidth - tolerant_area, 0))

        points.InsertNextPoint(((max_x - 80 + center[0]) * self.magnifyFactorWidth+tolerant_area,
                                (max_y - 80 + center[1]) * self.magnifyFactorWidth+tolerant_area, 0))

        points.InsertNextPoint(((min_x-80 + center[0]) * self.magnifyFactorWidth-tolerant_area,
                                (max_y-80 + center[1]) * self.magnifyFactorWidth+tolerant_area, 0))


        lines = vtk.vtkCellArray()
        lines.InsertNextCell(5)
        lines.InsertCellPoint(0)
        lines.InsertCellPoint(1)
        lines.InsertCellPoint(2)
        lines.InsertCellPoint(3)
        lines.InsertCellPoint(0)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        polydata.SetLines(lines)

        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputData(polydata)
        mapper.Update()

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1.0*colors[0]/255, 1.0*colors[1]/255, 1.0*colors[2]/255)
        actor.GetProperty().SetPointSize(5)

        self.renderer.AddActor2D(actor)
