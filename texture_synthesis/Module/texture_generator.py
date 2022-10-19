#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from tqdm import tqdm

from texture_synthesis.Method.patch import getRandomPatch, getRandomBestPatch, getMinCutPatch


class TextureGenerator(object):

    def __init__(self):
        return

    def generateTexture(self,
                        image_path,
                        patch_sample_percent,
                        num_block,
                        print_progress=False):
        assert os.path.exists(image_path)

        texture = cv2.imread(image_path)
        texture = texture / 255.0

        block_size = [
            int(texture.shape[i] * patch_sample_percent)
            for i in range(1, -1, -1)
        ]

        overlap = [block_size[i] // 6 for i in range(2)]

        block_width_num, block_height_num = num_block

        w = (block_width_num *
             block_size[0]) - (block_width_num - 1) * overlap[0]
        h = (block_height_num *
             block_size[1]) - (block_height_num - 1) * overlap[1]

        result = np.zeros((h, w, texture.shape[2]))

        block_num = block_width_num * block_height_num

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
                patch = getRandomBestPatch(texture, block_size, overlap,
                                           result, y, x)
                patch = getMinCutPatch(patch, overlap, result, y, x)

            result[y:y + block_size[1], x:x + block_size[0]] = patch

        image = (result * 255).astype(np.uint8)
        return image
