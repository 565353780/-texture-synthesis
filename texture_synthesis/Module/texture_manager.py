#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from tqdm import tqdm


class TextureManager(object):

    def __init__(self):
        return

    def renderRepeatTexture(self, texture, repeat_size):
        texture_shape = texture.shape[:2]

        repeat_texture = np.zeros((texture_shape[0] * repeat_size[1],
                                   texture_shape[1] * repeat_size[0], 3),
                                  dtype=np.uint8)

        repeat_num = repeat_size[0] * repeat_size[1]
        for repeat_idx in range(repeat_num):
            width_idx = repeat_idx // repeat_size[1]
            height_idx = repeat_idx % repeat_size[1]

            repeat_texture[height_idx * texture_shape[0]:(height_idx + 1) *
                           texture_shape[0],
                           width_idx * texture_shape[1]:(width_idx + 1) *
                           texture_shape[1]] = texture

        cv2.rectangle(repeat_texture, (0, 0), (texture_shape[1], texture_shape[0]), (0, 255, 0), 2)

        scale = 1.0
        if scale != 1.0:
            repeat_texture = cv2.resize(repeat_texture, None, fx=scale, fy=scale)
        return repeat_texture