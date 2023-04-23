#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np

from texture_synthesis.Method.cut import getSubImageDict
from texture_synthesis.Method.merge import mergeSubImagesWithMask


class ImageCutter(object):
    def __init__(self, width_expand=0.1, height_expand=0.1):
        self.width_expand = width_expand
        self.height_expand = height_expand
        return

    def cutImage(self, image):
        data = {
            'image': image,
            'width_expand': self.width_expand,
            'height_expand': self.height_expand
        }

        data = getSubImageDict(data)

        data = mergeSubImagesWithMask(data)

        mask_image = np.zeros_like(data['merged_image'], dtype=np.uint8)
        mask_image[data['mask']] = [255, 255, 255]

        cv2.imshow('merged_image', data['merged_image'])
        cv2.imshow('mask', mask_image)

        cv2.waitKey(0)
        return cut_image, mask

    def cutImageFile(self, image_file_path):
        assert os.path.exists(image_file_path)

        image = cv2.imread(image_file_path)
        return self.cutImage(image)
