#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from tqdm import tqdm

from texture_synthesis.Method.patch import getRandomPatch, getRandomBestPatch, getMinCutPatch


class TextureGenerator(object):

    def __init__(self):
        return

    def generateTexture(self,
                        image,
                        patch_sample_percent,
                        block_num_list,
                        print_progress=False):
        texture = image / 255.0

        block_size = [
            int(texture.shape[i] * patch_sample_percent)
            for i in range(1, -1, -1)
        ]

        overlap = [block_size[i] // 6 for i in range(2)]

        block_width_num, block_height_num = block_num_list

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

        generated_texture = (result * 255).astype(np.uint8)
        return generated_texture

    def generateWidthRepeatTexture(self, image, print_progress=False):
        texture = self.generateTexture(image, 1.0, (3, 1), print_progress)
        width_split = int(texture.shape[1] / 3.0)
        return texture[:, width_split:2 * width_split]

    def generateHeightRepeatTexture(self, image, print_progress=False):
        texture = self.generateTexture(image, 1.0, (1, 3), print_progress)
        height_split = int(texture.shape[0] / 3.0)
        return texture[height_split:2 * height_split, :]

    def generateWidthAndHeightRepeatTexture(self, image, print_progress=False):
        texture = self.generateTexture(image, 1.0, (3, 3), print_progress)
        width_split = int(texture.shape[1] / 3.0)
        height_split = int(texture.shape[0] / 3.0)
        return texture[height_split:2 * height_split,
                       width_split:2 * width_split]

    def generateRepeatTexture(self,
                              image,
                              width_repeat=True,
                              height_repeat=True,
                              print_progress=False):

        if width_repeat:
            if height_repeat:
                return self.generateWidthAndHeightRepeatTexture(
                    image, print_progress)
            return self.generateWidthRepeatTexture(image, print_progress)
        if height_repeat:
            return self.generateHeightRepeatTexture(image, print_progress)
