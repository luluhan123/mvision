#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
the class to represent a screen of the pc

author: Cheng WANG

last edited: February 2015
"""


class MSAScreen:
    def __init__(self):
        self.index = 0
        self.rect = None

    def set_index(self, index):
        self.index = index

    def get_index(self):
        return self.index

    def set_rect(self, rect):
        self.rect = rect

    def get_rect(self):
        return self.rect