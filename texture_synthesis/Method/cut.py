#!/usr/bin/env python
# -*- coding: utf-8 -*-


def getBlockImage(image, block_size, overlap, width_block_range,
                  height_block_range):
    width_idx_list = [
        int(width_block_range[i] * (block_size[0] - overlap[0]) +
            0.5 * overlap[0]) for i in range(2)
    ]

    height_idx_list = [
        int(height_block_range[i] * (block_size[1] - overlap[1]) +
            0.5 * overlap[1]) for i in range(2)
    ]

    return image[height_idx_list[0]:height_idx_list[1],
                 width_idx_list[0]:width_idx_list[1]]
