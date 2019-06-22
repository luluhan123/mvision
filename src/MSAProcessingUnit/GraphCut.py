#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
MainWindow of the IHM to contain all the graphic component

author: Heng QI

last edited: February 2015
"""
#import maxflow
from numpy import *
from math import *


class GraphCut:
    def __init__(self):
        self.initial_img = None

        self.ground_truth_point_set = None
        self.background_point_set = None

        self.input_img = None
        self.obj_bkg_lambda = 0.5
        self.pixel_sigma = 1000
        self.pixel_kappa = 5

    def set_ground_truth_point_set(self, ground_truth_point_set):
        self.ground_truth_point_set = ground_truth_point_set

    def set_background_point_set(self, background_point_set):
        self.background_point_set = background_point_set

    def set_input_img(self, input_img):
        self.input_img = input_img

    def compute_mean(self, pts):
        cpt = 0
        value = 0
        for pt in pts:
            value += self.initial_img[pt[0]][pt[1]]
            cpt += 1
        return (value*1.0/cpt)

    def execute(self):
        length = self.initial_img.shape[0]
        width = self.initial_img.shape[1]

        g = maxflow.Graph[float]()
        rp_obj = ones(self.initial_img.shape)
        rp_bkg = ones(self.initial_img.shape)
        nodes = g.add_nodes(length * width)

        obj_mean = self.compute_mean(self.ground_truth_point_set)
        bkg_mean = self.compute_mean(self.background_point_set)

        max_sum_b = 0.0

        for i in range(self.initial_img.shape[0]):  # Defining the Probability function....
            for j in range(self.initial_img.shape[1]):
                rp_obj[i, j] = -log(abs(self.initial_img[i, j] - obj_mean) / (abs(self.initial_img[i, j] - obj_mean) + abs(self.initial_img[i, j] - bkg_mean)))  # Probability of a pixel being foreground
                rp_bkg[i, j] = -log(abs(self.initial_img[i, j] - bkg_mean) / (abs(self.initial_img[i, j] - bkg_mean) + abs(self.initial_img[i, j] - obj_mean)))  # Probability of a pixel being background
        for i in range(self.initial_img.shape[0]):
            temp_max = 0.0
            for j in range(self.initial_img.shape[1]):
                if j != 0:
                    w_c = self.pixel_kappa * exp(-((float(self.initial_img[i, j]) - float(self.initial_img[i, j - 1])) * (float(self.initial_img[i, j]) - float(self.initial_img[i, j - 1]))) / self.pixel_sigma)
                    w_rc = w_c
                    temp_max = temp_max + w_c
                    g.add_edge(j + i * width, j + i * width - 1, w_c, w_rc)
                if j != width - 1:
                    w_c = self.pixel_kappa * exp(-((float(self.initial_img[i, j]) - float(self.initial_img[i, j + 1])) * (float(self.initial_img[i, j]) - float(self.initial_img[i, j + 1]))) / self.pixel_sigma)
                    w_rc = w_c
                    temp_max = temp_max + w_c
                    g.add_edge(j + i * width, j + i * width + 1, w_c, w_rc)
                if i != 0:
                    w_c = self.pixel_kappa * exp(-((float(self.initial_img[i, j]) - float(self.initial_img[i - 1, j])) * (float(self.initial_img[i, j]) - float(self.initial_img[i - 1, j]))) / self.pixel_sigma)
                    w_rc = w_c
                    temp_max = temp_max + w_c
                    g.add_edge(j + i * width, j + (i - 1) * width, w_c, w_rc)
                if i != length - 1:
                    w_c = self.pixel_kappa * exp(-((float(self.initial_img[i, j]) - float(self.initial_img[i + 1, j])) * (float(self.initial_img[i, j]) - float(self.initial_img[i + 1, j]))) / self.pixel_sigma)
                    w_rc = w_c
                    temp_max = temp_max + w_c
                    g.add_edge(j + i * width, j + (i + 1) * width, w_c, w_rc)
            if max_sum_b < temp_max:
                max_sum_b = temp_max
        big_k = 1 + max_sum_b

        for i in range(self.initial_img.shape[0]):
            for j in range(self.initial_img.shape[1]):
                    ws = (rp_obj[i, j] / (rp_obj[i, j] + rp_bkg[i, j]))  # source weight
                    wt = (rp_bkg[i, j] / (rp_obj[i, j] + rp_bkg[i, j]))  # sink weight
                    g.add_tedge(nodes[j + i * width], ws, wt)

        for pt in self.ground_truth_point_set:
            g.add_tedge(nodes[pt[1] + pt[0] * width], big_k, 0)

        for pt in self.background_point_set:
            g.add_tedge(nodes[pt[1] + pt[0] * width], 0, big_k)

        g.maxflow()
        segment_result = g.get_grid_segments(nodes)
        segment_result = segment_result.reshape(length, width)
        return segment_result