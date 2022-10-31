#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from tqdm import tqdm

from texture_synthesis.Method.patch import (getMinCutPatch, getRandomBestPatch,
                                            getRandomPatch)
from texture_synthesis.Method.trans import getBiggerImage


def generateTexture(image,
                    patch_sample_percent_list,
                    patch_overlap_percent_list,
                    block_num_list,
                    print_progress=False):
    texture = image / 255.0

    block_size = [
        int(texture.shape[1 - i] * patch_sample_percent_list[i])
        for i in range(2)
    ]

    overlap = [
        int(block_size[i] * patch_overlap_percent_list[i]) for i in range(2)
    ]

    block_width_num, block_height_num = block_num_list

    w = (block_width_num * block_size[0]) - (block_width_num - 1) * overlap[0]
    h = (block_height_num *
         block_size[1]) - (block_height_num - 1) * overlap[1]

    result = np.zeros((h, w, texture.shape[2]))

    block_num = block_width_num * block_height_num

    error_sum = 0

    for_data = range(block_num)
    if print_progress:
        print("[INFO][TextureGenerator::generateTexture]")
        print("\t start generate texture...")
        for_data = tqdm(for_data)
    for block_idx in for_data:
        width_idx = block_idx // block_height_num
        height_idx = block_idx % block_height_num

        x = width_idx * (block_size[0] - overlap[0])
        y = height_idx * (block_size[1] - overlap[1])

        if width_idx == 0 and height_idx == 0:
            patch = getRandomPatch(texture, block_size)
        else:
            patch = getRandomBestPatch(texture, block_size, overlap, result, y,
                                       x)
            patch, error = getMinCutPatch(patch, overlap, result, y, x)
            error_sum += error

        result[y:y + block_size[1], x:x + block_size[0]] = patch

    generated_texture = (result * 255).astype(np.uint8)
    return generated_texture, block_size, overlap, error_sum


def generateBestTexture(image,
                        patch_sample_percent_list,
                        patch_overlap_percent_list,
                        block_num_list,
                        print_progress=False):
    scale = 0.1
    expand_scale_list_list = [
        [0, 0],
        [scale, scale],
    ]
    bigger_image = getBiggerImage(image, expand_scale_list_list)
    exit()

    min_error = float('inf')
    best_generated_texture = None
    best_block_size = None
    best_overlap = None

    for i in range(1, overlap_sample_num):
        patch_overlap_percent_list = [
            1.0 * i / overlap_sample_num, 1.0 * i / overlap_sample_num
        ]
        generated_texture, block_size, overlap, error_sum = generateTexture(
            image, patch_sample_percent_list, patch_overlap_percent_list,
            block_num_list, print_progress)
        print(error_sum)
        if error_sum < min_error:
            print(min_error, "->", error_sum)
            min_error = error_sum
            best_generated_texture = generated_texture
            best_block_size = block_size
            best_overlap = overlap
    return best_generated_texture, best_block_size, best_overlap, min_error
