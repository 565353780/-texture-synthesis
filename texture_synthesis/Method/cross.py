#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy

from texture_synthesis.Data.patch import Patch


def isPatchCross(patch_1, patch_2):
    if patch_1.start_pixel.x >= patch_2.end_pixel.x:
        return False
    if patch_1.start_pixel.y >= patch_2.end_pixel.y:
        return False
    if patch_2.start_pixel.x >= patch_1.end_pixel.x:
        return False
    if patch_2.start_pixel.y >= patch_1.end_pixel.y:
        return False
    return True


def isPatchCrossPatches(patch, patch_list):
    for target_patch in patch_list:
        if isPatchCross(patch, target_patch):
            return True
    return False


def getBiggestNoCrossPatch(patch_list, image_width, image_height):
    if len(patch_list) == 0:
        return None
    if len(patch_list) == 1:
        return patch_list[0]

    min_x = float('inf')
    min_y = float('inf')
    start_patch_idx = -1

    for i, patch in enumerate(patch_list):
        x_min = patch.start_pixel.x
        y_min = patch.start_pixel.y
        if x_min + y_min < min_x + min_y:
            min_x = min(min_x, x_min)
            min_y = min(min_y, y_min)
            start_patch_idx = i

    biggest_no_cross_patch = patch_list[start_patch_idx]

    check_cross_patch_list = []
    end_x_list = []
    end_y_list = []
    for i, patch in enumerate(patch_list):
        if i == start_patch_idx:
            continue
        end_x_list.append(patch.start_pixel.x)
        end_y_list.append(patch.start_pixel.y)
        check_cross_patch_list.append(patch)

    patch_expanded = True
    while patch_expanded:
        patch_expanded = False
        for end_x in end_x_list:
            if end_x <= biggest_no_cross_patch.end_pixel.x:
                continue
            for end_y in end_y_list:
                if end_y <= biggest_no_cross_patch.end_pixel.y:
                    continue

                max_x = max(biggest_no_cross_patch.end_pixel.x, end_x)
                max_y = max(biggest_no_cross_patch.end_pixel.y, end_y)
            expand_patch = Patch.fromList([[min_x, min_y], [max_x, max_y]])
            if isPatchCrossPatches(expand_patch, check_cross_patch_list):
                continue
            biggest_no_cross_patch = expand_patch
            patch_expanded = True
            break

    max_x = max(biggest_no_cross_patch.end_pixel.x, image_width)
    max_y = max(biggest_no_cross_patch.end_pixel.y, image_height)
    width_height_expand_patch = Patch.fromList([[min_x, min_y], [max_x,
                                                                 max_y]])
    if not isPatchCrossPatches(width_height_expand_patch,
                               check_cross_patch_list):
        return width_height_expand_patch

    max_x = max(biggest_no_cross_patch.end_pixel.x, image_width)
    max_y = biggest_no_cross_patch.end_pixel.y
    width_expand_patch = Patch.fromList([[min_x, min_y], [max_x, max_y]])
    width_expand_patch_area = width_expand_patch.getArea()

    max_x = biggest_no_cross_patch.end_pixel.x
    max_y = max(biggest_no_cross_patch.end_pixel.y, image_height)
    height_expand_patch = Patch.fromList([[min_x, min_y], [max_x, max_y]])
    height_expand_patch_area = height_expand_patch.getArea()

    if width_expand_patch_area >= height_expand_patch_area:
        if not isPatchCrossPatches(width_expand_patch, check_cross_patch_list):
            return width_expand_patch
        if not isPatchCrossPatches(height_expand_patch,
                                   check_cross_patch_list):
            return height_expand_patch
    else:
        if not isPatchCrossPatches(height_expand_patch,
                                   check_cross_patch_list):
            return height_expand_patch
        if not isPatchCrossPatches(width_expand_patch, check_cross_patch_list):
            return width_expand_patch

    return biggest_no_cross_patch
