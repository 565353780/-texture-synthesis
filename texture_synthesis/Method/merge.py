#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def mergeSubImagesWithMask(data):
    image = data['image']
    width_expand = data['width_expand']
    height_expand = data['height_expand']
    first_width = data['first_width']
    first_height = data['first_height']
    second_width = data['second_width']
    second_height = data['second_height']
    left_up = data['left_up']
    right_up = data['right_up']
    left_down = data['left_down']
    right_down = data['right_down']

    image_width = first_width + second_width
    image_height = first_height + second_height

    expand_half_width = max(int(image_width * width_expand / 2.0), 1)
    expand_half_height = max(int(image_height * height_expand / 2.0), 1)

    merged_image_width = image_width + expand_half_width * 2
    merged_image_height = image_height + expand_half_height * 2

    if len(image.shape) == 3:
        merged_image = np.zeros(
            [merged_image_width, merged_image_height, image.shape[2]],
            dtype=np.uint8)
    else:
        merged_image = np.zeros([merged_image_width, merged_image_height],
                                dtype=np.uint8)

    merge_second_width_start = second_width + expand_half_width * 2
    merge_second_height_start = second_height + expand_half_height * 2

    merged_image[:second_width, :second_height] = right_down
    merged_image[merge_second_width_start:, :second_height] = left_down
    merged_image[:second_width, merge_second_height_start:] = right_up
    merged_image[merge_second_width_start:,
                 merge_second_height_start:] = left_up

    mask = np.zeros([merged_image_width, merged_image_height], dtype=bool)
    mask[second_width:merge_second_width_start, :] = True
    mask[:, second_height:merge_second_height_start] = True

    data['expand_half_width'] = expand_half_width
    data['expand_half_height'] = expand_half_height
    data['merge_second_width_start'] = merge_second_width_start
    data['merge_second_height_start'] = merge_second_height_start
    data['merged_image'] = merged_image
    data['mask'] = mask
    return data


def recombineMergedImage(data):
    first_width = data['first_width']
    first_height = data['first_height']
    second_width = data['second_width']
    second_height = data['second_height']
    expand_half_width = data['expand_half_width']
    expand_half_height = data['expand_half_height']
    complete_merged_image = data['complete_merged_image']

    expand_first_width = first_width + expand_half_width
    expand_first_height = first_height + expand_half_height
    expand_second_width = second_width + expand_half_width
    expand_second_height = second_height + expand_half_height

    recombined_image = np.zeros_like(complete_merged_image, dtype=np.uint8)

    recombined_image[:expand_first_width, :
                     expand_first_height] = complete_merged_image[
                         expand_second_width:, expand_second_height:]
    recombined_image[
        expand_first_width:, :
        expand_first_height] = complete_merged_image[:expand_second_width,
                                                     expand_second_height:]
    recombined_image[:expand_first_width,
                     expand_first_height:] = complete_merged_image[
                         expand_second_width:, :expand_second_height]
    recombined_image[
        expand_first_width:,
        expand_first_height:] = complete_merged_image[:expand_second_width, :
                                                      expand_second_height]

    data['recombined_image'] = recombined_image
    return data
