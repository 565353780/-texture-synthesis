#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2

from texture_synthesis.Module.texture_generator import TextureGenerator


def demo():
    image_file_path = "./data/input1.jpg"
    image_file_path = "/home/chli/chLi/texture/flower.png"
    patch_sample_percent = 0.3
    block_num_list = (4, 4)
    print_progress = True

    assert os.path.exists(image_file_path)
    image = cv2.imread(image_file_path)

    texture_generator = TextureGenerator()
    generated_texture = texture_generator.generateTexture(
        image, patch_sample_percent, block_num_list, print_progress)

    width_repeat_texture = texture_generator.generateRepeatTexture(
        image, height_repeat=False, print_progress=print_progress)

    height_repeat_texture = texture_generator.generateRepeatTexture(
        image, width_repeat=False, print_progress=print_progress)

    repeat_texture = texture_generator.generateRepeatTexture(
        image, print_progress)

    cv2.imshow("generated_texture", generated_texture)
    cv2.imshow("width_repeat_texture", width_repeat_texture)
    cv2.imshow("height_repeat_texture", height_repeat_texture)
    cv2.imshow("repeat_texture", repeat_texture)
    cv2.waitKey(0)
    return True
