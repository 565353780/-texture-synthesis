#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy


def fillMergedImage(data, fill_color=[0, 255, 0]):
    merged_image = data['merged_image']
    mask = data['mask']

    complete_merged_image = deepcopy(merged_image)

    if len(merged_image.shape) == 3:
        complete_merged_image[mask] = fill_color
    else:
        complete_merged_image[mask] = 128

    data['complete_merged_image'] = complete_merged_image
    return data
