#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
MainWindow of the IHM to contain all the graphic component

author: Cheng WANG

last edited: February 2015
"""

from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QFrame, QSlider, QHBoxLayout, QPushButton, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QSize, Qt

from src.MSAModel.MSAStructure.MSAPoint import MSAPoint
from src.MSAView.MSAMainWindow.MSAImageWorkSpace.MSACanvas2D import MSACanvas2D
from src.MSAView.MSAMainWindow.IHMTool.MSAPlottingBoard import MSAPlottingBoard
from src.MSAView.MSAMainWindow.MSAImageWorkSpace.ResultViewer import ResultViewer
from src.MSAView.MSAMainWindow.MSAImageWorkSpace.MSAInformationArea import MSAInformationArea

import vtk
import matplotlib
import time
import os
import numpy as np
import math
import cv2
import scipy.misc as misc
import scipy.misc


class MSAWorkSpace(QFrame):
    doVesselEnhancement = pyqtSignal()
    doClearScreens = pyqtSignal()
    returnPressed = pyqtSignal()
    updateCurrentSequence = pyqtSignal(str)
    buttonMessage = pyqtSignal(str)
    closeSignal = pyqtSignal()
    minimizeSignal = pyqtSignal()
    maximizeSignal = pyqtSignal()
    vesselSegmentationWindow = pyqtSignal()
    parameterWindowSetting = pyqtSignal()

    def interpolation(self, pts, resolution):

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

        pts_nbr = spline_source.GetOutput().GetNumberOfPoints()
        pts_in_polydata = spline_source.GetOutput()

        ret = []

        for i in range(pts_nbr):
            pt = MSAPoint(0, pts_in_polydata.GetPoint(i)[0], pts_in_polydata.GetPoint(i)[1])
            ret.append(pt)

        return ret

    # [1] patch area tracking
    def do_track_guidewire(self, img, i):
        # ignore the tracking gravity points which has been removed
        if i in self.removed_sequence:
            return

        # get part image according to the predefined radius, if in
        self.possiblely_gravity_points[i], patch = self.controller.get_part_image_by_size(img, self.possiblely_gravity_points[i], self.global_tacking_area_radius * 2 + 1)
        # pt, patch_for_display = self.controller.get_part_image_by_size_by_vtk(self.ctSequenceViewer.current_x_ray_image.get_values(), self.possiblely_gravity_points[i], self.global_tacking_area_radius * 2 + 1, self.global_tacking_area_radius * 2 + 1, 512, 512)
        # self.ctSequenceAnalyseArea.display_numpy_image(self.controller.frangi_img(patch))
        # matplotlib.image.imsave('/home/cheng/Desktop/hehe/' + str(self.ctSequenceViewer.display_count) + '.png', self.controller.frangi_img(patch), cmap=matplotlib.cm.gray)

        # self.ctSequenceAnalyseArea.display_frangi(patch_for_display)
        # ridge point extraction based on tube filter
        ridge_pts = self.controller.san_ban_fu(patch)

        if (len(ridge_pts) / self.global_patch_size) > 0.009:
            self.removed_sequence.append(i)
            return

        # noise points removal
        ridge_pts_filtered = []
        for pt in ridge_pts:
            if self.maximumLikelyhoodTrackingArea[i][int(pt[0])][int(pt[1])] > 0:
                ridge_pts_filtered.append((pt[0], pt[1]))

        # eliminate points which are too far from the guidewire tip structure in last frame
        ridge_pts_calibrated = []
        if len(self.possiblely_guidewire_tip_structure[i]) > 3:
            for pt in ridge_pts_filtered:
                if self.find_nearest_distance(pt, self.possiblely_guidewire_tip_structure[i][-1]):
                    ridge_pts_calibrated.append(pt)
        else:
            ridge_pts_calibrated = ridge_pts_filtered

        if len(ridge_pts_calibrated) == 0:
            self.removed_sequence.append(i)
            return

        temp = []
        for pt in ridge_pts_calibrated:
            temp.append(img[pt[0]][pt[1]])
        interval = max(temp) - min(temp)
        grayscale_threshold = min(temp) + interval*0.1
        ridge_pts_sorted = []
        for pt in ridge_pts_calibrated:
            if img[pt[0]][pt[1]] > grayscale_threshold:
                ridge_pts_sorted.append(pt)

        ridge_pts_new = self.controller.curve_fitting(ridge_pts_sorted, 8, self.global_tacking_area_radius * 2 + 1, self.global_tacking_area_radius * 2 + 1, 8)
        if ridge_pts_new is not None:
            ridge_pts_new.sort()
            #self.possiblely_guidewire_tip_structure[i] = ridge_pts_new.interpolation(10)
            self.possiblely_guidewire_tip_structure[i].append(self.interpolation(ridge_pts_new, 10))
        else:
            self.removed_sequence.append(i)
            return

        color = QColor(self.color[i])
        # self.ctSequenceViewer.key_points_display(self.guidewire_tip_sequence[i], self.possible_points[i], (color.red(), color.green(), color.blue()), self.global_tacking_area_radius)
        # self.ctSequenceViewer.tuple_points_display(ridge_pts_filtered, self.possiblely_gravity_points[i], (255, 0, 0), 80)
        # self.ctSequenceViewer.key_points_display(self.possible_sequences[i], self.possible_points[i], (color.red(), color.green(), color.blue()), self.global_tacking_area_radius)
        # self.ctSequenceViewer.draw_a_single_point(self.possible_sequences[i], self.possible_points[i], (color.red(),color.green(), color.blue()), self.global_tacking_area_radius)
        # self.ctSequenceViewer.curve_display(self.possiblely_guidewire_tip_structure[i], self.possible_points[i], (color.red(), color.green(), color.blue()))
        # print (i, time.time())
        # self.save_random_points(self.mask_contour[i], self.possible_points[i],  self.ctSequenceViewer.display_count)
        # self.save_guidewire_tip_ground_truth(self.possiblely_guidewire_tip_structure[i], self.possiblely_gravity_points[i], self.ctSequenceViewer.display_count, i)
        #
        # --------------------------------------------------------visualization work-------------------------------------------------------------------------------------------------
        # [1]
        # self.ctSequenceViewer.draw_tuple_point_cloud_by_order(ridge_pts, self.possiblely_gravity_points[i], (255, 165, 0), 80)

        # [2]
        # self.ctSequenceViewer.draw_tuple_point_cloud_by_order(ridge_pts_filtered, self.possiblely_gravity_points[i], (255, 250, 250), 80)

        # [3]
        # self.ctSequenceViewer.contour_key_points_display(self.maximumLikelyhoodTrackingAreaMask[i], self.possiblely_gravity_points[i], (color.red(), color.green(), color.blue()), self.global_tacking_area_radius)

        # [4]
        self.ctSequenceViewer.generate_box_and_display(self.possiblely_gravity_points[i], self.global_tacking_area_radius * 2, self.global_tacking_area_radius * 2, (color.red(), color.green(), color.blue()))

        # [5]
        if len(self.possiblely_guidewire_tip_structure[i]) > 2:
            if self.ctSequenceViewer.display_count < 36:
                #self.ctSequenceViewer.draw_point_cloud_by_order(self.possiblely_guidewire_tip_structure[i][-2], self.possiblely_gravity_points[i], QColor(153, 255, 255), self.global_tacking_area_radius)
                self.ctSequenceViewer.draw_point_cloud_by_order(self.possiblely_guidewire_tip_structure[i][-1], self.possiblely_gravity_points[i], color, self.global_tacking_area_radius)
            else:
                #self.ctSequenceViewer.draw_point_cloud_by_order(self.possiblely_guidewire_tip_structure[i][-2], self.possiblely_gravity_points[i], QColor(107, 227, 207), self.global_tacking_area_radius)
                self.ctSequenceViewer.draw_point_cloud_by_order(self.possiblely_guidewire_tip_structure[i][-1], self.possiblely_gravity_points[i], QColor(239, 188, 64), self.global_tacking_area_radius)
                #self.ctSequenceViewer.curve_display(self.possiblely_guidewire_tip_structure[i][-1], self.possiblely_gravity_points[i], (239, 188, 64))

        # mov = self.predict_movement(ridge_pts_filtered, 80)
        mov = self.predict_movement(self.possiblely_guidewire_tip_structure[i][-1], self.global_tacking_area_radius)

        self.maximumLikelyhoodTrackingArea[i], self.maximumLikelyhoodTrackingAreaMask[i] = self.compute_convex_hull(self.possiblely_guidewire_tip_structure[i][-1], 30, self.global_tacking_area_radius * 2 + 1, self.global_tacking_area_radius * 2 + 1)

        self.possiblely_gravity_points[i] = (int(self.possiblely_gravity_points[i][0] + mov[0]), int(self.possiblely_gravity_points[i][1] + mov[1]))

        self.predict_sequence[i].append(self.possiblely_gravity_points[i])
        # print ("image:", self.ctSequenceViewer.display_count, "possiblity:",i,  "gravities:", self.predict_sequence[i])
        if (self.possiblely_gravity_points[i][0] > self.abscissa) or (self.possiblely_gravity_points[i][0] < 0) or (self.possiblely_gravity_points[i][1] > self.ordinate) or (self.possiblely_gravity_points[i][1] < 0):
            self.removed_sequence.append(i)
            return

        if len(self.predict_sequence[i]) > 3 and self.compute_distance(self.predict_sequence[i][-1], self.predict_sequence[i][-2]) > 63:
            # print ("err value", self.compute_distance(self.predict_sequence[i][-1],self.predict_sequence[i][-2]))
            self.removed_sequence.append(i)
            return

        if self.ctSequenceViewer.display_count > 0:
            for x in range(self.initial_possibility):
                if x not in self.removed_sequence:
                    if x != i:
                        if self.compute_distance(self.predict_sequence[i][-1], self.predict_sequence[x][-1]) < 10:
                            self.removed_sequence.append(i)
                            return

        if self.ctSequenceViewer.display_count > 1:
            distance = float(math.sqrt((self.possiblely_gravity_points[i][0] - self.predict_sequence[i][1][0]) ** 2 + (self.possiblely_gravity_points[i][1] - self.predict_sequence[i][1][1]) ** 2))
            self.predict_sequence_movements[i].append(distance)

        if self.ctSequenceViewer.display_count == self.predict_threshold:
            self.predict_sequence_deviation.append((self.compute_standard_deviation(self.predict_sequence_movements[i], self.compute_means(self.predict_sequence_movements[i])), i))

    def execute(self):
        self.ctSequenceAnalyseArea.clear()

        # convert image from vtk to numpy
        total_img = self.controller.set_image_to_numpyy(self.ctSequenceViewer.current_x_ray_image.get_values())
        #self.ctSequenceAnalyseArea.display_numpy_image(self.controller.frangi_img(total_img))
        #matplotlib.image.imsave('/home/cheng/Desktop/hehe/' + str(self.ctSequenceViewer.display_count) + '.png', self.controller.frangi_img(total_img), cmap=matplotlib.cm.gray)

        self.abscissa, self.ordinate = np.shape(total_img)
        if self.ctSequenceViewer.display_count == 0:

            global_ridge_pts = self.controller.san_ban_fu(total_img)
            self.ctSequenceViewer.global_key_points_display(global_ridge_pts, (80, 80), [255.0, 120.0, 0.0], 80)
            self.possiblely_gravity_points = self.controller.do_predict_possible_points(global_ridge_pts)

            self.initial_possibility = len(self.possiblely_gravity_points)
            self.ctSequenceViewer.points_display(self.possiblely_gravity_points, [0, 0, 255], 10)
            for x in range(self.initial_possibility):
                self.possiblely_guidewire_tip_structure.append([])
                self.predict_sequence.append([])
                self.predict_sequence_movements.append([])
                self.maximumLikelyhoodTrackingArea.append(np.ones((self.global_tacking_area_radius * 2 + 1, self.global_tacking_area_radius * 2 + 1)))
                self.maximumLikelyhoodTrackingAreaMask.append([])
                self.guidewire_tip_sequence.append([])
                self.curve_sequence_historical.append([])

        for i in range(self.initial_possibility):
            self.do_track_guidewire(total_img, i)

        if self.ctSequenceViewer.display_count == self.predict_threshold:
            deviation_seq = []
            # print(self.predict_sequence_deviation)
            for pair in self.predict_sequence_deviation:
                deviation_seq.append(pair[0])
            print("maximum Deviation", max(deviation_seq), "all", deviation_seq)
            index = deviation_seq.index(max(deviation_seq))
            for i in range(len(deviation_seq)):
                if i != index:
                    self.removed_sequence.append(self.predict_sequence_deviation[i][1])

        self.imageVisualizationConfigurationArea.do_plot_distance_flow(self.predict_sequence_movements)

        self.ctSequenceAnalyseArea.update_all()

    def distance(self, pt0, pt1):
        return math.sqrt((pt1.get_x() - pt0[0]) ** 2 + (pt1.get_y() - pt0[1]) ** 2)

    def find_nearest_distance(self, pt, pts):
        distances = []
        for p in pts:
            distances.append(self.distance(pt, p))
        length = len(distances)
        temp = min(distances)
        temp_index = distances.index(temp)
        if (temp_index == 0 and temp > 20) or (temp_index == length - 1 and temp > 20):
            return False
        else:
            return True

    def clear_current_file(self):
        index = int(self.processSliderIndicationLabel.text())
        path = "C:\\Users\\cheng\\Desktop\\savePoints\\"
        filenames = os.listdir(path)
        filenames.sort()

        for filename in filenames:
            deleteFilename = str(index) + '_'
            if filename.__contains__(deleteFilename):
                newPath = path + "\\" + filename
                os.remove(newPath)
                self.file_num = 0

    def save_current_frame_point(self):
        if_change_frame = int(self.processSliderIndicationLabel.text())
        index = int(self.processSliderIndicationLabel.text())

        current_x_ray_image = self.controller.get_image_by_index(index)
        current_frame_point = current_x_ray_image.get_guidewire_tip()

        path = "C:\\Users\\cheng\\Desktop\\savePoints\\"
        file_name = str(index) + '_' + str(self.file_num) + ".txt"
        f = open(path + file_name, 'w')
        f.write(str(current_frame_point))
        f.close()
        self.file_num += 1

    def find_grayscale_peak(self, pt, patch, tolerant_area_radius):
        x1 = pt[0] - tolerant_area_radius
        y1 = pt[1] - tolerant_area_radius
        x2 = pt[0] + tolerant_area_radius
        y2 = pt[1] + tolerant_area_radius
        peak_point = pt
        for i in range(x1, x2):
            for j in range(y1, y2):
                if patch[i, j] > patch[peak_point[0], peak_point[1]]:
                    peak_point = [i, j]
        return peak_point

    def predict_movement(self, pts, radius):
        point_x = list()
        point_y = list()
        for i in pts:
            point_x.append(i.get_x())
            point_y.append(i.get_y())
        mean_point_x = round(np.mean(point_x))
        mean_point_y = round(np.mean(point_y))

        return mean_point_x - radius, mean_point_y - radius

    def save_random_points(self, pts, centre, index):
        filename = "D:\\projet\\GTT\\contour" + str(index) + ".csv"
        if index == 15:
            print(centre)
        with open(filename, 'w') as fileobject:
            for pt in pts:
                fileobject.write(str((pt[0] + centre[0] - 80)) + ";" + str((pt[1] + centre[1] - 80)) + "\n")
        fileobject.close()

    def save_guidewire_tip_ground_truth(self, pts, centre, index, i):
        file_name = "/home/cheng/Desktop/9/" + self.global_sequence_name + "_" + str(10000 + index) + "_" + str(i) + ".csv"
        with open(file_name, 'w') as fileobject:
            for c in range(len(pts)):
                fileobject.write(str((pts[c].get_x() + centre[0] - 80)) + ";" + str((pts[c].get_y() + centre[1] - 80)) + "\n")
        fileobject.close()

    def calculate_min_distance(self, pts):
        distances = []
        for index in range(len(pts) - 1):
            distance = float(math.sqrt((pts[index][0] - pts[index + 1][0]) ** 2 + (pts[index][1] - pts[index + 1][1]) ** 2))
            distances.append(distance)
        return min(distances)

    def insert(self, pts):
        new_pts = []
        for index in range(len(pts) - 1):
            new_pts.append(pts[index])
            distance = float(math.sqrt((pts[index][0] - pts[index + 1][0]) ** 2 + (pts[index][1] - pts[index + 1][1]) ** 2))
            if distance > 0.15:
                new_pts.append(((pts[index][0] - pts[index + 1][0]) / 2, (pts[index][1] - pts[index + 1][1]) / 2))
        return new_pts

    def compute_distance(self, pt0, pt1):
        return math.sqrt((pt1[0] - pt0[0]) ** 2 + (pt1[1] - pt0[1]) ** 2)

    def change_slider_value(self, value):
        if self.ctSequenceViewer.is_ready():
            self.flag = False
            if self.doGuidewireTracking:
                self.execute()
            else:
                time.sleep(0.1)
            self.current_image_index = value
            self.processSlider.setValue(value)
            self.processSliderIndicationLabel.setText(str(value))

    def update_current_tooltip(self, tooltip):
        self.buttonMessage.emit(tooltip)

    def update_current_sequence_information(self, sequence_info):
        self.global_sequence_name = sequence_info
        self.updateCurrentSequence.emit(sequence_info)

    def target_image_choosing_back_button_clicked(self):
        self.file_num = 0
        index = int(self.processSliderIndicationLabel.text())
        if index - 1 >= 0:
            self.ctSequenceViewer.do_display_by_index(index - 1)
            self.processSlider.setValue(index - 1)
            self.processSliderIndicationLabel.setText(str(index - 1))

    def target_image_choosing_button_clicked(self):
        self.file_num = 0
        index = int(self.processSliderIndicationLabel.text())
        if index + 1 <= self.controller.get_current_sequence_count() - 1:
            self.ctSequenceViewer.do_display_by_index(index + 1)
            self.processSlider.setValue(index + 1)
            self.processSliderIndicationLabel.setText(str(index + 1))

    def process_slider_indication_label_pressed(self):
        index = self.processSliderIndicationLabel.text().toInt()[0]
        self.ctSequenceViewer.do_display_by_index(index)
        self.processSlider.setValue(index)

    def do_vessel_enhancement(self):
        x_ray_image = self.ctSequenceViewer.get_current_x_ray_image()

        if x_ray_image is None:
            return

        total_img = self.controller.set_image_to_numpyy(x_ray_image.get_values())
        enhanced_image = self.controller.frangi_img(total_img)

        if (enhanced_image.max() <= 1) and (enhanced_image.min() >= 0):
            enhanced_image = enhanced_image * 255

        self.ctSequenceAnalyseArea.display_frangi(self.controller.convertt(enhanced_image))

    def contour_extraction(self, img):
        img = np.array(img).astype(np.uint8)
        blurred = cv2.GaussianBlur(img, (11, 11), 0)
        edged = cv2.Canny(blurred, 0.5, 1.5)
        (_, conts, _) = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return conts

    def do_save_pts(self, pts, img_index, posibility):
        temp = '/home/cheng/Documents/' + self.global_sequence_name + '-' + str(img_index) + '--' + str(posibility) + '.csv'
        f = open(temp, 'w')
        for l in pts:
            f.write(str(l[0]) + ';' + str(l[1]) + '\n')
        f.close()

    def do_save_part_image(self, img, img_index, posibility):
        writer = vtk.vtkPNGWriter()
        writer.SetFileName('/home/cheng/Documents/' + self.global_sequence_name + '-' + str(img_index) + '--' + str(posibility) + '.png')
        writer.SetInputData(img)
        writer.Write()

    def do_save_part_image_numpy(self, img, img_index, posibility):
        img = img[::-1]
        scipy.misc.imsave('/home/cheng/Documents/' + self.global_sequence_name + '-' + str(img_index) + '--' + str(posibility) + 'mask' + '.png', img)

    def clear_screen(self):
        self.controller.reinitialiser_base_de_donnee()
        self.ctSequenceViewer.nettoyer()
        self.ctSequenceViewer.mise_a_jour()
        self.imageVisualizationConfigurationArea.clear()
        self.imageVisualizationConfigurationArea.update()
        self.ctSequenceAnalyseArea.clear_all()
        self.ctSequenceAnalyseArea.update()
        self.processSlider.setValue(0)
        self.processSliderIndicationLabel.setText('0')
        self.displayButtonClicked = False

    def set_global_voi(self, w, h):
        self.ctSequenceViewer.set_global_voi(w, h)

    def set_global_window_and_level(self, window, level):
        self.window = window
        self.level = level
        self.ctSequenceViewer.set_global_window_and_level(window, level)
        self.ctSequenceAnalyseArea.set_global_window_and_level(window, level)

    def enable_guidewire_tracking(self):
        self.doGuidewireTracking = not self.doGuidewireTracking

    def set_image_sequence_loaded(self):
        self.ctSequenceViewer.set_image_sequence_loaded()

    def update_x_ray_sequences(self):
        self.parameterVisualizeArea.update_x_ray_sequences()

    def set_process_slider(self, files_count):
        self.processSlider.setMinimum(0)
        self.processSlider.setMaximum(files_count - 1)
        self.total_image_count = files_count

    def visualise_files(self):
        self.ctSequenceAnalyseArea.clear_all_picture()
        folder_path = self.controller.get_current_sequence_icon_folder()
        for image in sorted(os.listdir(folder_path)):
            if image.endswith(".png"):
                self.ctSequenceAnalyseArea.add_a_picture(image.split('.')[0], folder_path + image)

    def do_plot_histogram(self, img_in_vtk):
        statistics = vtk.vtkImageHistogramStatistics()
        statistics.SetInputData(img_in_vtk)
        statistics.GenerateHistogramImageOff()
        statistics.Update()

        maximal_grayscale = statistics.GetMaximum()
        minimal_grayscale = statistics.GetMinimum()
        histogram = statistics.GetHistogram()

        range_value = maximal_grayscale - minimal_grayscale
        grayscales = []
        frequency = []

        for i in range(int(range_value)):

            if i == 0:
                continue

            index = int(minimal_grayscale) + i
            grayscales.append(index)
            frequency.append(histogram.GetValue(i))

        self.imageVisualizationConfigurationArea.plot(grayscales, frequency)

    def compute_means(self, seq):
        sum = 0
        for v in seq:
            sum += v
        return sum / len(seq)

    def compute_standard_deviation(self, seq, mean):
        sum = 0
        for v in seq:
            sum += (v - mean) ** 2
        return sum / len(seq)

    def do_execute_rpca(self):
        if self.ctSequenceViewer.display_count >= 5:
            temp_img1 = self.controller.get_image_by_index(self.ctSequenceViewer.display_count - 1)
            temp_img2 = self.controller.get_image_by_index(self.ctSequenceViewer.display_count - 2)
            temp_img3 = self.controller.get_image_by_index(self.ctSequenceViewer.display_count - 3)
            temp_img4 = self.controller.get_image_by_index(self.ctSequenceViewer.display_count - 4)
            temp_img5 = self.controller.get_image_by_index(self.ctSequenceViewer.display_count - 5)

            self.convert_temp_img1 = self.controller.set_image_to_numpyy(temp_img1.get_values())
            self.convert_temp_img2 = self.controller.set_image_to_numpyy(temp_img2.get_values())
            self.convert_temp_img3 = self.controller.set_image_to_numpyy(temp_img3.get_values())
            self.convert_temp_img4 = self.controller.set_image_to_numpyy(temp_img4.get_values())
            self.convert_temp_img5 = self.controller.set_image_to_numpyy(temp_img5.get_values())

            self.converted_image1 = self.convert_temp_img1.reshape(512 * 512, 1)
            self.converted_image2 = self.convert_temp_img2.reshape(512 * 512, 1)
            self.converted_image3 = self.convert_temp_img3.reshape(512 * 512, 1)
            self.converted_image4 = self.convert_temp_img4.reshape(512 * 512, 1)
            self.converted_image5 = self.convert_temp_img5.reshape(512 * 512, 1)

            self.converted_image = np.column_stack((self.converted_image1,
                                                    self.converted_image2,
                                                    self.converted_image3,
                                                    self.converted_image4,
                                                    self.converted_image5))

            A, E = self.controller.execute_rpca(self.converted_image)

            output_img = E[:, 4].reshape((512, 512))
            mask = output_img > 0
            output_img[mask] = 0

            output_data = np.zeros((512, 512))
            for l in range(512):
                for h in range(512):
                    if output_img[l][h] < 0:
                        output_data[l][h] = abs(output_img[h][l])
                    else:
                        output_data[l][h] = output_img[l][h]

            output_data = (1.0 * 255 * output_data) / np.amax(output_data)

            # print output_data

            vtk_img_E = self.controller.convertt(output_img)

            # vtk_img_A = self.controller.convertt(self.A.reshape((512, 512)))
            # self.A = (1.0 * 255* self.A) / np.amax(self.A)

            self.ctSequenceAnalyseArea.frangiViewer.display_rpca_vtk_image(vtk_img_E)
            # self.ctSequenceAnalyseArea.localFrangiViewer.displayRpcaVTKImage(vtk_img_A)

    def execute_ridgepoint_extraction(self):
        input_img = self.ctSequenceViewer.current_x_ray_image.get_values * ()
        none_zero_index = self.controller.execute_ridgepoint_extraction(input_img)
        self.ctSequenceViewer.ridge_point(none_zero_index)

    # def ridge_point_extraction_key_area(self):
    #     key_area_none_zero_index = self.controller.ridge_point_extraction_key_area()

    def cal_Score(self, input):
        l = np.size(input, axis=0)
        z = np.polyfit(input[:, 0], input[:, 1], 3)
        p = np.poly1d(z)
        sum = 0
        for i in range(l):
            sum += abs(p(input[i, 0]) - input[i, 1])
        sum = sum / l
        return sum

    def do_save_tracking_image(self, tracked_image):
        writer = vtk.vtkMetaImageWriter()
        writer.SetInputData(tracked_image)
        writer.SetCompression(False)
        writer.SetFileName('/home/cheng/Desktop/tracked_area/' + str(self.ctSequenceViewer.display_count) + '.mhd')
        writer.SetRAWFileName('/home/cheng/Desktop/tracked_area/' + str(self.ctSequenceViewer.display_count) + '.raw')
        writer.Write()

    def amplify_img_view(self, flag):
        if flag:
            self.ctSequenceAnalyseArea.close()
            self.imageVisualizationConfigurationArea.close()

        else:
            self.ctSequenceAnalyseArea.show()
            self.imageVisualizationConfigurationArea.show()
        return

    def modify_window_value(self, flag):
        if flag:
            self.ctSequenceViewer.modifier_display_size(self.ct_img_view_width, self.ct_img_view_height)
        else:
            self.ctSequenceViewer.restore_display_size()

        return self.window_width, self.window_height

    def segment_current_image(self):
        self.ctSequenceAnalyseArea.display_frangi(self.ctSequenceViewer.enhance_guide_wire())
        self.ctSequenceAnalyseArea.display_local_frangi(self.ctSequenceViewer.local_frangi())

    def do_frangi(self):
        return self.ctSequenceViewer.enhance_guide_wire()

    def do_local_frangi(self):
        return self.ctSequenceViewer.local_frangi()

    def close_gui(self):
        self.imageVisualizationConfigurationArea.disconnect_event()
        self.closeSignal.emit()

    def maximize_gui(self):
        self.maximizeSignal.emit()

    def minimize_gui(self):
        self.minimizeSignal.emit()

    def set_process_slider_value(self, v):
        self.processSlider.setValue(0)

    def display_button_clicked(self):
        if self.displayButtonClicked:
            self.ctSequenceViewer.pause_image_sequence()
            self.displayButton.setIcon(QIcon(":/falltoolbar.png"))
        else:
            self.ctSequenceViewer.display_image_sequence()
            self.displayButton.setIcon(QIcon(":/beforeplay.png"))

        self.displayButtonClicked = not self.displayButtonClicked

    def show_coordinate_state_changed(self, flag):
        self.ctSequenceViewer.show_coordinate_enable(flag)

    def show_gray_state_changed(self, flag):
        self.ctSequenceViewer.enable_show_gray(flag)

    def screen_shot_state_changed(self, flag):
        self.ctSequenceViewer.enabled_screen_shot(flag)

    def tracer_points_state_changed(self, flag):
        self.ctSequenceViewer.enabled_tracer_points(flag)

    def initial_points_sign_state_changed(self, flag):
        self.ctSequenceViewer.enable_initial_points_sign(flag)

    def tracer_box_state_changed(self, flag):
        self.ctSequenceViewer.enable_box_tracer(flag)

    def measure_distance_state_changed(self, flag):
        self.ctSequenceViewer.enabled_distance_mea(flag)

    def img_rotation_state_changed(self, flag):
        self.ctSequenceViewer.enable_img_rotation(flag)

    def generate_curve_state_changed(self, flag):
        self.ctSequenceViewer.enable_generate_curve(flag)

    def clear_analyse_window(self):
        self.ctSequenceAnalyseArea.imageProcessingViewer.clear()

    def tracking_image_display(self, centre, img, mag_x, mag_y):
        self.ctSequenceAnalyseArea.imageProcessingViewer.clear()
        self.ctSequenceAnalyseArea.imageProcessingViewer.display_image_by_factor(centre, img, mag_x, mag_y)

    def marked_points_display(self, current_point, point_sequence, flag, width_ratio, height_ratio, pts_size, color):
        self.ctSequenceAnalyseArea.imageProcessingViewer.marked_points_display(current_point, point_sequence, width_ratio, height_ratio, pts_size, color)
        self.ctSequenceAnalyseArea.imageProcessingViewer.update()

    def vessel_segmention_window_setting(self):
        self.vesselSegmentationWindow.emit()

    def parameter_window_setting(self):
        self.parameterWindowSetting.emit()

    def update_background_color(self, color_string):
        color = QColor(color_string)
        self.ctSequenceViewer.update_background_color(color.red(), color.green(), color.blue())
        self.ctSequenceAnalyseArea.update_background_color(color_string)
        self.parameterVisualizeArea.update_background_color(color_string)
        self.imageVisualizationConfigurationArea.update_background_color(color_string)
        self.controlBar.setStyleSheet("background-color: " + color_string)

    def enable_vascular_button_clicked(self, click_flag):
        self.parameterVisualizeArea.enable_vascular_button_clicked(click_flag)

    def enable_paraset_button_clicked(self, click_flag):
        self.parameterVisualizeArea.enable_paraset_button_clicked(click_flag)

    def vascular_button_icon_change(self):
        self.parameterVisualizeArea.vascular_button_icon_change()

    def paraset_button_icon_change(self):
        self.parameterVisualizeArea.paraset_button_icon_change()

    # def execute_Rpca(self):
    #     if self.ctSequenceViewer.display_count >= 1:
    #
    #         self.current_x_ray_image = self.controller.get_image_by_index(self.ctSequenceViewer.display_count - 1)
    #         self.convert_image = self.controller.set_image_to_numpyy(self.current_x_ray_image.get_values())
    #         self.converted_image = self.convert_image.reshape(512 * 512, 1)
    #
    #         self.A, self.E = self.controller.execute_Rpca(self.converted_image)
    #
    #         vtk_img_E = self.controller.convertt(self.E.reshape((512, 512)))
    #         # print self.E[:,4].shape
    #         # vtk_img_E = self.controller.convertt(self.E[:,4].reshape((512,512)))
    #
    #         # vtk_img_A = self.controller.convertt(self.A.reshape((512, 512)))
    #         # self.A = (1.0 * 255* self.A) / np.amax(self.A)
    #
    #         self.ctSequenceAnalyseArea.frangiViewer.displayRpcaVTKImage(vtk_img_E)
    #         # self.ctSequenceAnalyseArea.localFrangiViewer.displayRpcaVTKImage(vtk_img_A)
    def compute_convex_hull(self, possible_sequences, exploreArea, limit_x, limit_y):
        x = []
        y = []
        for item in possible_sequences:
            x.append(item.get_x())
            y.append(item.get_y())
        value_matrix = np.zeros([limit_x, limit_y])
        hull_points = []
        if len(x) > 0:
            for index in range(0, len(x)):
                x1 = int(x[index] - exploreArea)
                y1 = int(y[index] - exploreArea)
                x2 = int(x[index] + exploreArea + 1)
                y2 = int(y[index] + exploreArea + 1)
                if 0 <= x1 < limit_x and 0 <= y1 < limit_y and 0 <= x2 < limit_x and 0 <= y2 < limit_y:
                    for i in range(x1, x2):
                        for j in range(y1, y2):
                            distance = int(self.compute_distance((x[index], y[index]), (i, j)))
                            if distance == exploreArea and value_matrix[i][j] != 1:
                                value_matrix[i][j] = 2
                            if distance < exploreArea:
                                value_matrix[i][j] = 1

        for i in range(0, limit_x):
            for j in range(0, limit_y):
                if value_matrix[i][j] == 2:
                    hull_points.append((i, j))
        return value_matrix, hull_points

    def connexion(self):
        self.displayButton.clicked.connect(self.display_button_clicked)
        self.targetImageChoosingBackButton.clicked.connect(self.target_image_choosing_back_button_clicked)
        self.targetImageChoosingButton.clicked.connect(self.target_image_choosing_button_clicked)
        self.processSliderIndicationLabel.returnPressed.connect(self.process_slider_indication_label_pressed)
        self.ctSequenceAnalyseArea.doClearScreens.connect(self.clear_screen)
        self.parameterVisualizeArea.doVesselEnhancement.connect(self.do_vessel_enhancement)
        self.parameterVisualizeArea.buttonMessage.connect(self.update_current_tooltip)
        self.ctSequenceViewer.newImageSequenceDropped[str].connect(self.update_current_sequence_information)
        self.ctSequenceAnalyseArea.buttonMessage[str].connect(self.update_current_tooltip)
        self.parameterVisualizeArea.parameterWindowSetting.connect(self.parameter_window_setting)
        self.parameterVisualizeArea.vesselSegmentationWindow.connect(self.vessel_segmention_window_setting)
        self.ctSequenceAnalyseArea.mesaureDistanceState.connect(self.measure_distance_state_changed)
        self.ctSequenceAnalyseArea.coordinateState.connect(self.show_coordinate_state_changed)
        self.ctSequenceAnalyseArea.tracerBoxState.connect(self.tracer_box_state_changed)
        self.ctSequenceAnalyseArea.tracerPointsState.connect(self.tracer_points_state_changed)
        self.ctSequenceAnalyseArea.initialPointsSign.connect(self.initial_points_sign_state_changed)
        self.clearPointButton.clicked.connect(self.save_current_frame_point)
        self.clearPointfileButton.clicked.connect(self.clear_current_file)

    def __init__(self, parent=None, controller=None, ihm_factor=1, width=0, height=0, background_color="", global_font_color="", global_font=None, target_image_width=0, target_image_height=0):
        super(MSAWorkSpace, self).__init__()

        # -------------------------------------------------------------------------------------------------------------------
        # parameter passed
        # -------------------------------------------------------------------------------------------------------------------
        self.parent = parent
        self.controller = controller
        self.ihm_factor = ihm_factor
        self.width = width
        self.height = height
        self.previous_image = None
        self.previous_ridge = None
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font
        self.target_image_width = target_image_width
        self.target_image_height = target_image_height

        self.file_num = 0

        self.point_save = []

        # -------------------------------------------------------------------------------------------------------------------
        # initialise variable
        # -------------------------------------------------------------------------------------------------------------------
        self.flag = True
        self.ct_img_view_width = self.width * 0.85
        self.ct_img_view_height = self.height - self.height * 0.6 * 0.05

        self.window_width = 0
        self.window_height = 0
        self.setFixedSize(width, height)
        self.setStyleSheet("background-color:" + self.globalBackgroundColor + "; color:" + self.globalFontColor + ";")

        self.A = None
        self.E = None
        self.convert_temp_img1 = np.zeros((512, 512))
        self.convert_temp_img2 = np.zeros((512, 512))
        self.convert_temp_img3 = np.zeros((512, 512))
        self.convert_temp_img4 = np.zeros((512, 512))
        self.convert_temp_img5 = np.zeros((512, 512))

        self.converted_image1 = np.zeros((512 * 512, 1))
        self.converted_image2 = np.zeros((512 * 512, 1))
        self.converted_image3 = np.zeros((512 * 512, 1))
        self.converted_image4 = np.zeros((512 * 512, 1))
        self.converted_image5 = np.zeros((512 * 512, 1))

        self.convert_image = np.zeros((512, 512))
        self.converted_image = np.zeros((512 * 512, 1))

        self.possiblely_gravity_points = list()
        self.possiblely_guidewire_tip_structure = list()

        self.predict_sequence = []
        self.predict_sequence_movements = []
        self.predict_sequence_deviation = []

        self.threshold = 0
        self.total_image_count = 0
        self.initial_possibility = 3
        self.removed_sequence = []
        self.abscissa = 0
        self.ordinate = 0

        self.predict_threshold = 36

        # -------------------------------------------------------------------------------------------------------------------
        # construction of the IHM
        # -------------------------------------------------------------------------------------------------------------------
        self.parameterVisualizeArea = MSAInformationArea(self,
                                                         self.controller,
                                                         self.ihm_factor,
                                                         256 * self.ihm_factor,
                                                         self.height,
                                                         self.globalBackgroundColor,
                                                         self.globalFontColor,
                                                         self.globalFont)

        self.ctSequenceViewerWidth = self.target_image_width * self.ihm_factor
        self.ctSequenceViewerHeight = self.target_image_height * self.ihm_factor

        self.ctSequenceViewer = MSACanvas2D(self,
                                            self.controller,
                                            self.ihm_factor,
                                            self.ctSequenceViewerWidth,
                                            self.ctSequenceViewerHeight,
                                            self.target_image_width,
                                            self.target_image_height,
                                            self.globalBackgroundColor,
                                            self.globalFontColor,
                                            self.globalFont)

        self.displayButton = QPushButton()
        self.displayButton.setStyleSheet("background: " + self.globalBackgroundColor)
        self.displayButton.setIcon(QIcon(":/beforeplay.png"))
        self.displayButton.setMouseTracking(True)
        self.displayButton.setFixedSize(QSize(20 * self.ihm_factor, 20 * self.ihm_factor))
        self.displayButton.setIconSize(QSize(20 * self.ihm_factor, 20 * self.ihm_factor))
        self.displayButton.setFlat(True)

        self.clearPointButton = QPushButton()
        self.clearPointButton.setStyleSheet("background: " + self.globalBackgroundColor)
        self.clearPointButton.setIcon(QIcon(":/beforeplay.png"))
        self.clearPointButton.setMouseTracking(True)
        self.clearPointButton.setFixedSize(QSize(20 * self.ihm_factor, 20 * self.ihm_factor))
        self.clearPointButton.setIconSize(QSize(20 * self.ihm_factor, 20 * self.ihm_factor))
        self.clearPointButton.setFlat(True)

        self.clearPointfileButton = QPushButton()
        self.clearPointfileButton.setStyleSheet("background: " + self.globalBackgroundColor)
        self.clearPointfileButton.setIcon(QIcon(":/close.png"))
        self.clearPointfileButton.setMouseTracking(True)
        self.clearPointfileButton.setFixedSize(QSize(20 * self.ihm_factor, 20 * self.ihm_factor))
        self.clearPointfileButton.setIconSize(QSize(20 * self.ihm_factor, 20 * self.ihm_factor))
        self.clearPointfileButton.setFlat(True)

        self.processSlider = QSlider(Qt.Horizontal)
        self.processSlider.setFixedSize(self.ctSequenceViewerWidth - 150, 18 * self.ihm_factor)
        self.processSlider.setStyleSheet("QSlider::add-page:Horizontal{background-color: rgb(87, 97, 106);height:4px;} "
                                         "QSlider::sub-page:Horizontal{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(146,181,50, 255), stop:1 rgba(23,108,87, 255));height:4px;} "
                                         "QSlider::groove:Horizontal{ background:transparent; height:6px;}"
                                         "QSlider::handle:Horizontal{height: 30px; width:8px; border-image: url(:/images/ic_music_thumb.png); margin: -8 0px; }")

        self.targetImageChoosingBackButton = QPushButton()
        self.targetImageChoosingBackButton.setIcon(QIcon(":/subpoint.png"))
        self.targetImageChoosingBackButton.setFixedSize(18 * self.ihm_factor, 18 * self.ihm_factor)
        self.targetImageChoosingBackButton.setIconSize(QSize(18 * self.ihm_factor, 18 * self.ihm_factor))
        self.targetImageChoosingBackButton.setFlat(True)

        self.processSliderIndicationLabel = QLineEdit("0")
        self.processSliderIndicationLabel.setFixedSize(25 * self.ihm_factor, 18 * self.ihm_factor)
        self.processSliderIndicationLabel.setFont(self.globalFont)
        self.processSliderIndicationLabel.setStyleSheet("border:0px solid orange; color: " + self.globalFontColor)
        self.processSliderIndicationLabel.setAlignment(Qt.AlignCenter)

        self.targetImageChoosingButton = QPushButton()
        self.targetImageChoosingButton.setIcon(QIcon(":/addpoint.png"))
        self.targetImageChoosingButton.setFixedSize(18 * self.ihm_factor, 18 * self.ihm_factor)
        self.targetImageChoosingButton.setIconSize(QSize(18 * self.ihm_factor, 18 * self.ihm_factor))
        self.targetImageChoosingButton.setFlat(True)

        self.controlBar = QLabel()
        self.controlBar.setStyleSheet("background-color:" + self.globalBackgroundColor + "; color:" + self.globalFontColor)
        self.controlBar.setFixedHeight(20 * self.ihm_factor)
        self.controlBarLayout = QHBoxLayout(self.controlBar)
        self.controlBarLayout.addWidget(self.displayButton)
        self.controlBarLayout.addWidget(self.processSlider)
        self.controlBarLayout.addWidget(self.targetImageChoosingBackButton)
        self.controlBarLayout.addWidget(self.processSliderIndicationLabel)
        self.controlBarLayout.addWidget(self.targetImageChoosingButton)
        # self.controlBarLayout.addWidget(self.clearPointButton)
        # self.controlBarLayout.addWidget(self.clearPointfileButton)
        self.controlBarLayout.setSpacing(1)
        self.controlBarLayout.setContentsMargins(0, 0, 0, 0)

        self.imageVisualizationConfigurationArea = MSAPlottingBoard(2, self.controller, self.ihm_factor, self.ctSequenceViewerWidth, 256 * self.ihm_factor, self.globalBackgroundColor, self.globalFontColor, self.globalFont)

        self.ctSequenceViewerArea = QFrame()
        self.ctSequenceViewerArea.setStyleSheet("background-color: " + self.globalBackgroundColor)
        self.ctSequenceViewerAreaLayout = QVBoxLayout(self.ctSequenceViewerArea)
        self.ctSequenceViewerAreaLayout.addWidget(self.ctSequenceViewer)
        self.ctSequenceViewerAreaLayout.addWidget(self.controlBar)
        self.ctSequenceViewerAreaLayout.addWidget(self.imageVisualizationConfigurationArea)
        self.ctSequenceViewerAreaLayout.setSpacing(0)
        self.ctSequenceViewerAreaLayout.setContentsMargins(0, 0, 0, 0)

        self.ctSequenceAnalyseArea = ResultViewer(self, self.controller, self.ihm_factor, self.ctSequenceViewerWidth, self.height, self.target_image_width, self.target_image_height, self.globalBackgroundColor, self.globalFontColor, self.globalFont)

        self.main_window = QFrame(self)
        self.main_window.setFixedSize(self.width, self.height)
        self.myLayout = QHBoxLayout(self.main_window)
        self.myLayout.addWidget(self.parameterVisualizeArea)
        self.myLayout.addWidget(self.ctSequenceViewerArea)
        self.myLayout.addWidget(self.ctSequenceAnalyseArea)
        self.myLayout.setContentsMargins(0, 0, 0, 0)
        self.myLayout.setSpacing(0)

        self.displayButtonClicked = False
        self.doGuidewireTracking = False
        self.window = 1000
        self.level = 0
        self.color = ['red', 'yellow', 'blue', 'green', 'white', 'magenta']
        self.maximumLikelyhoodTrackingArea = []
        self.maximumLikelyhoodTrackingAreaMask = []
        self.guidewire_tip_sequence = []
        self.global_sequence_name = ""
        self.current_image_index = 0
        self.global_tacking_area_radius = 80
        self.global_patch_size = (self.global_tacking_area_radius * 2) ** 2
        self.curve_sequence_historical = []

        # -------------------------------------------------------------------------------------------------------------------
        # signal/slots
        # -------------------------------------------------------------------------------------------------------------------
        self.connexion()
