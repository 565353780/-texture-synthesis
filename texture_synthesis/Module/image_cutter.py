#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2


class ImageCutter(object):
    def __init__(self):
        return

    def cutImage(self, image):
        return cut_image, mask

    def cutImageFile(self, image_file_path):
        assert os.path.exists(image_file_path)

        image = cv2.imread(image_file_path)
        return self.cutImage(image)
