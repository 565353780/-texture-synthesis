#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from copy import deepcopy
from multiprocessing import Pool

import cv2
import numpy as np
from tqdm import tqdm

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


def getBestMatchPatch(image, patch):
    patch_image = getPatchImage(image, patch)
    if patch_image is None:
        return None, -1

    x_min = patch.start_pixel.x
    y_min = patch.start_pixel.y
    x_max = patch.end_pixel.x
    y_max = patch.end_pixel.y

    search_image = deepcopy(image)
    search_image[y_min:y_max, x_min:x_max, :] = 0

    similar_matrix = cv2.matchTemplate(search_image, patch_image,
                                       cv2.TM_CCOEFF_NORMED)

    _, match_score, _, start_pixel = cv2.minMaxLoc(similar_matrix)

    best_match_patch = Patch.fromList(
        [[start_pixel[0], start_pixel[1]],
         [start_pixel[0] + x_max - x_min, start_pixel[1] + y_max - y_min]])
    return best_match_patch, match_score


def getAllBestMatchPatch(image, patch, min_match_score=0.5, max_match_num=-1):
    best_match_patch_list = []
    match_score_list = []

    search_image = deepcopy(image)

    best_match_score = -float('inf')

    while True:
        best_match_patch, match_score = getBestMatchPatch(search_image, patch)
        best_match_score = max(best_match_score, match_score)
        if match_score < min_match_score or \
                match_score < min_match_score * best_match_score:
            break

        best_match_patch_list.append(best_match_patch)
        match_score_list.append(match_score)

        if max_match_num > 0 and len(best_match_patch_list) == max_match_num:
            break

        x_min = best_match_patch.start_pixel.x
        y_min = best_match_patch.start_pixel.y
        x_max = best_match_patch.end_pixel.x
        y_max = best_match_patch.end_pixel.y
        search_image[y_min:y_max, x_min:x_max, :] = 0

    return best_match_patch_list, match_score_list


def getBestMatchPatchList(image,
                          patch_percent_list,
                          min_match_score=0.5,
                          max_match_num=-1,
                          print_progress=False):
    best_match_patch_list = []
    best_match_score = -float('inf')
    if len(patch_percent_list) == 0:
        return best_match_patch_list, best_match_score

    image_height, image_width, _ = image.shape

    for patch_percent in patch_percent_list:
        patch_width = int(patch_percent * image_width)
        patch_height = int(patch_percent * image_height)
        for_data = range(0, image_width, patch_width)
        if print_progress:
            print("[INFO][dist::getBestMatchPatchList]")
            print("\t start check patch percent :", patch_percent, "...")
            for_data = tqdm(for_data)
        for x in for_data:
            for y in range(0, image_height, patch_height):
                patch = Patch.fromList([[x, y],
                                        [x + patch_width, y + patch_height]])
                current_best_match_patch_list, match_score_list = getAllBestMatchPatch(
                    image, patch, min_match_score, max_match_num)
                if len(current_best_match_patch_list) == 0:
                    continue

                mean_match_score = np.mean(match_score_list)
                if mean_match_score > best_match_score:
                    best_match_score = mean_match_score
                    best_match_patch_list = current_best_match_patch_list
    return best_match_patch_list, best_match_score
