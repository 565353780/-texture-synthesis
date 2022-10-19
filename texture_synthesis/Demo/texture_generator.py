#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

from texture_synthesis.Module.texture_generator import TextureGenerator


def demo():
    image_path = "./data/input1.jpg"
    image_path = "/home/chli/chLi/texture/flower.png"
    patch_sample_percent = 0.3
    num_block = (4, 4)
    print_progress = True

    texture_generator = TextureGenerator()
    generated_texture = texture_generator.generateTexture(
        image_path, patch_sample_percent, num_block, print_progress)

    width_repeat_texture = texture_generator.generateRepeatTexture(
        image_path, height_repeat=False, print_progress=print_progress)

    height_repeat_texture = texture_generator.generateRepeatTexture(
        image_path, width_repeat=False, print_progress=print_progress)

    repeat_texture = texture_generator.generateRepeatTexture(
        image_path, print_progress)

    cv2.imshow("generated_texture", generated_texture)
    cv2.imshow("width_repeat_texture", width_repeat_texture)
    cv2.imshow("height_repeat_texture", height_repeat_texture)
    cv2.imshow("repeat_texture", repeat_texture)
    cv2.waitKey(0)
    return True
