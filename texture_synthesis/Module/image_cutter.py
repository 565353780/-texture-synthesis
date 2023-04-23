#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np

from texture_synthesis.Method.cut import getSubImageDict


class ImageCutter(object):
    def __init__(self, width_expand=0.1, height_expand=0.1):
        self.width_expand = width_expand
        self.height_expand = height_expand
        return

    def cutImage(self, image):
        sub_image_dict = getSubImageDict(image)

        first_width = sub_image_dict['first_width']
        first_height = sub_image_dict['first_height']
        second_width = sub_image_dict['second_width']
        second_height = sub_image_dict['second_height']

        left_up = np.zeros_like(image, dtype=np.uint8)
        left_up[:first_width, :first_height] = sub_image_dict['left_up']

        right_up = np.zeros_like(image, dtype=np.uint8)
        right_up[first_width:, :first_height] = sub_image_dict['right_up']

        left_down = np.zeros_like(image, dtype=np.uint8)
        left_down[:first_width, first_height:] = sub_image_dict['left_down']

        right_down = np.zeros_like(image, dtype=np.uint8)
        right_down[first_width:, first_height:] = sub_image_dict['right_down']

        cv2.imshow('left_up', left_up)
        cv2.imshow('right_up', right_up)
        cv2.imshow('left_down', left_down)
        cv2.imshow('right_down', right_down)

        cv2.waitKey(0)
        return cut_image, mask

    def cutImageFile(self, image_file_path):
        assert os.path.exists(image_file_path)

        image = cv2.imread(image_file_path)
        return self.cutImage(image)
