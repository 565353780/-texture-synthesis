#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

from texture_synthesis.Method.cut import getBlockImage
from texture_synthesis.Method.texture import generateBiggerTexture

from texture_synthesis.Module.texture_optimizer import TextureOptimizer


def demo():
    image_file_path = "/home/chli/chLi/texture/Image/图片/11.jpg"
    image = cv2.imread(image_file_path)

    texture_optimizer = TextureOptimizer()

    patch_sample_percent_list = [1.0, 1.0]
    patch_overlap_percent_list = [0.2, 0.2]
    block_num_list = [3, 3]
    scale_max_list = [0.5, 0.5, 0.5, 0.5]
    render_bigger_image = False
    wait_key = 0
    width_block_range = [1, 2]
    height_block_range = [1, 2]
    print_progress = True

    best_scale_list = texture_optimizer.getBestScaleList(
        image, patch_sample_percent_list, patch_overlap_percent_list,
        block_num_list, scale_max_list, print_progress)

    print("best_scale_list:")
    print(best_scale_list)

    texture, block_size, overlap, error_sum = generateBiggerTexture(
        image, patch_sample_percent_list, patch_overlap_percent_list,
        block_num_list, best_scale_list, render_bigger_image, wait_key,
        print_progress)

    print("error_sum:")
    print(error_sum)

    repeat_texture = getBlockImage(texture, block_num_list, block_size,
                                   overlap, width_block_range,
                                   height_block_range)
    cv2.imshow("repeat_texture", repeat_texture)
    cv2.waitKey(0)
    return True
