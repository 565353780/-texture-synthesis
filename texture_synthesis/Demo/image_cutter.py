#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2

from texture_synthesis.Module.image_cutter import ImageCutter


def demo():
    width_expand = 0.1
    height_expand = 0.1
    image_file_path = '/home/chli/chLi/tt1.png'

    image_cutter = ImageCutter(width_expand, height_expand)

    mode = 'data'
    assert mode in ['file', 'data']
    if mode == 'file':
        data = image_cutter.cutImageFile(image_file_path)
    elif mode == 'data':
        assert os.path.exists(image_file_path)
        image = cv2.imread(image_file_path)
        data = image_cutter.cutImage(image)

    data = image_cutter.recombineImage(data)

    cv2.imshow('image', data['image'])
    cv2.imshow('complete_merged_image', data['complete_merged_image'])
    cv2.imshow('recombined_image', data['recombined_image'])
    cv2.waitKey(0)
    return True
