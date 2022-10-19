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

        texture_shape = texture.shape[:2]

        block_size = int(np.min(texture_shape) * patch_sample_percent)

        overlap = block_size // 6

        block_width_num, block_height_num = num_block

        w = (block_width_num * block_size) - (block_width_num - 1) * overlap
        h = (block_height_num * block_size) - (block_height_num - 1) * overlap

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

            x = width_idx * (block_size - overlap)
            y = height_idx * (block_size - overlap)

            if width_idx == 0 and height_idx == 0:
                patch = getRandomPatch(texture, block_size)
            else:
                patch = getRandomBestPatch(texture, block_size, overlap,
                                           result, y, x)
                patch = getMinCutPatch(patch, overlap, result, y, x)

            result[y:y + block_size, x:x + block_size] = patch

        image = (result * 255).astype(np.uint8)
        return image
