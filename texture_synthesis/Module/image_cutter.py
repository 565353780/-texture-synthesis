#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
from copy import deepcopy

from texture_synthesis.Method.cut import getSubImageDict
from texture_synthesis.Method.merge import mergeSubImagesWithMask, recombineMergedImage


def testEditMergedImage(data):
    merged_image = data['merged_image']
    mask = data['mask']

    complete_merged_image = deepcopy(merged_image)
    complete_merged_image[mask] = [0, 255, 0]

    data['complete_merged_image'] = complete_merged_image
    return data


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
        return data

    def recombineImage(self, data):
        if 'complete_merged_image' not in data.keys():
            print('[WARN][ImageCutter::recombineImage]')
            print(
                '\t complete_merged_image not exist! will fill it as green color!'
            )
            print('\t you need to append it into the input dict!')
            data = testEditMergedImage(data)

        data = recombineMergedImage(data)
        return data

    def cutImageFile(self, image_file_path):
        assert os.path.exists(image_file_path)

        image = cv2.imread(image_file_path)
        return self.cutImage(image)
