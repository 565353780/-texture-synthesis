#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from tqdm import trange
from multiprocessing import Pool

from texture_synthesis.Data.patch import Patch


def isPatchInImage(image, patch):
    image_height, image_width, _ = image.shape

    x_min = patch.start_pixel.x
    y_min = patch.start_pixel.y
    x_max = patch.end_pixel.x
    y_max = patch.end_pixel.y

    if x_min < 0 or x_min >= image_width:
        return False
    if y_min < 0 or y_min >= image_height:
        return False
    if x_max < 0 or x_max >= image_width:
        return False
    if y_max < 0 or y_max >= image_height:
        return False
    return True


def isSamePatch(patch_1, patch_2):
    if patch_1.start_pixel.x != patch_2.start_pixel.x:
        return False
    if patch_1.start_pixel.y != patch_2.start_pixel.y:
        return False
    if patch_1.end_pixel.x != patch_2.end_pixel.x:
        return False
    if patch_1.end_pixel.y != patch_2.end_pixel.y:
        return False
    return True


def getPatchImage(image, patch):
    if not isPatchInImage(image, patch):
        return None

    x_min = patch.start_pixel.x
    y_min = patch.start_pixel.y
    x_max = patch.end_pixel.x
    y_max = patch.end_pixel.y

    patch_image = image[y_min:y_max, x_min:x_max]
    return patch_image


def getPatchDist(image, patch_1, patch_2):
    patch_image_1 = getPatchImage(image, patch_1)
    patch_image_2 = getPatchImage(image, patch_2)

    if patch_image_1 is None or patch_image_2 is None:
        return float('inf')

    if isSamePatch(patch_1, patch_2):
        return float('inf')

    patch_diff = patch_image_1 - patch_image_2
    patch_abs_diff = np.absolute(patch_diff)
    patch_dist = np.sum(patch_abs_diff)
    return patch_dist


def getPatchDistWithPool(inputs):
    image, patch_1, patch_2 = inputs
    patch_1 = Patch.fromList(patch_1)
    patch_2 = Patch.fromList(patch_2)
    return getPatchDist(image, patch_1, patch_2)


def getPatchDistMatrix(image, patch_size):
    patch_dist_matrix = np.zeros((image_width, image_height))
    for x in trange(image_width):
        for y in range(image_height):
            patch_1 = Patch.fromList(
                [[x, y], [x + search_patch_size, y + search_patch_size]])
            for p in range(image_width):
                for q in range(image_height):
                    if p == x and q == y:
                        continue
                    patch_2 = Patch.fromList(
                        [[p, q],
                         [p + search_patch_size, q + search_patch_size]])

                    patch_dist_matrix[x][y] = getPatchDist(
                        image, patch_1, patch_2)
    return patch_dist_matrix


def getPatchDistMatrixWithPool(image, patch_size):
    image_height, image_width, _ = image.shape

    inputs_list = []

    for x in trange(image_width):
        for y in range(image_height):
            patch_1 = [[x, y], [x + patch_size, y + patch_size]]
            for p in range(image_width):
                for q in range(image_height):
                    patch_2 = [[p, q], [p + patch_size, q + patch_size]]
                    inputs_list.append([image, patch_1, patch_2])

    with Pool(os.cpu_count()) as pool:
        result = list(
            tqdm(pool.imap(getPatchDistWithPool, inputs_list),
                 total=len(inputs_list)))

    patch_dist_matrix = np.array(result).reshape(image_width, image_height)
    return patch_dist_matrix
