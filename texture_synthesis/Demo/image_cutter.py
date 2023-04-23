#!/usr/bin/env python
# -*- coding: utf-8 -*-

from texture_synthesis.Module.image_cutter import ImageCutter


def demo():
    image_file_path = '/home/chli/chLi/tt1.png'

    image_cutter = ImageCutter()

    data = image_cutter.cutImageFile(image_file_path)
    return True
