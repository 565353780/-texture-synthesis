#!/usr/bin/env python
# -*- coding: utf-8 -*-

from texture_synthesis.Module.image_cutter import ImageCutter


def demo():
    image_file_path = '/home/chli/chLi/test.jpg'

    image_cutter = ImageCutter()

    cut_image, mask = image_cutter.cutImageFile(image_file_path)
    return True
