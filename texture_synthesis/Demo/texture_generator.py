#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

from texture_synthesis.Module.texture_generator import TextureGenerator


def demo():
    image_path = "./data/input1.jpg"
    block_size = 192
    num_block = (4, 3)
    print_progress = True

    texture_generator = TextureGenerator()
    image = texture_generator.generateTexture(image_path, block_size,
                                              num_block, print_progress)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    return True
