#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy


def getBlockImage(image, block_num_list, block_size, overlap,
                  width_block_range, height_block_range):
    width_idx_list = [
        int(width_block_range[i] * (block_size[0] - overlap[0]) +
            0.5 * overlap[0]) for i in range(2)
    ]

    if width_block_range[0] == 0:
        width_idx_list[0] = 0
    if width_block_range[1] == block_num_list[0]:
        width_idx_list[1] = image.shape[1]

    height_idx_list = [
        int(height_block_range[i] * (block_size[1] - overlap[1]) +
            0.5 * overlap[1]) for i in range(2)
    ]

    if height_block_range[0] == 0:
        height_idx_list[0] = 0
    if height_block_range[1] == block_num_list[1]:
        height_idx_list[1] = image.shape[0]

    return image[height_idx_list[0]:height_idx_list[1],
                 width_idx_list[0]:width_idx_list[1]]


def getSubImageDict(data):
    image = data['image']

    width, height = image.shape[:2]
    first_width = int(width / 2.0)
    first_height = int(height / 2.0)

    left_up = deepcopy(image[:first_width, :first_height])
    right_up = deepcopy(image[first_width:, :first_height])
    left_down = deepcopy(image[:first_width, first_height:])
    right_down = deepcopy(image[first_width:, first_height:])

    data['first_width'] = first_width
    data['first_height'] = first_height
    data['second_width'] = width - first_width
    data['second_height'] = height - first_height
    data['left_up'] = left_up
    data['right_up'] = right_up
    data['left_down'] = left_down
    data['right_down'] = right_down
    return data
