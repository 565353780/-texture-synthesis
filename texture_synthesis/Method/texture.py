#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from tqdm import tqdm

from texture_synthesis.Method.patch import getMinCutPatch, getRandomBestPatch, getRandomPatch


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
            error += error_sum

        result[y:y + block_size[1], x:x + block_size[0]] = patch

    generated_texture = (result * 255).astype(np.uint8)
    return generated_texture, block_size, overlap, error_sum
