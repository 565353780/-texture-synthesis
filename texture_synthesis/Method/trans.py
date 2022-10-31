#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from texture_synthesis.Method.matrix import getTransMatrix
from texture_synthesis.Method.render import renderTransImageBox


def getBiggerPointPairList(image_width, image_height, expand_scale_list_list):
    assert 3 <= len(expand_scale_list_list) <= 4

    leftup_point_pair = [[0, 0],
                         [
                             -expand_scale_list_list[0][1] * image_height,
                             -expand_scale_list_list[0][0] * image_width
                         ]]

    rightup_point_pair = [[0, image_width],
                          [
                              -expand_scale_list_list[1][1] * image_height,
                              image_width +
                              expand_scale_list_list[1][0] * image_width
                          ]]

    leftdown_point_pair = [[image_height, 0],
                           [
                               image_height +
                               expand_scale_list_list[2][1] * image_height,
                               -expand_scale_list_list[2][0] * image_width
                           ]]

    if len(expand_scale_list_list) == 3:
        return [leftup_point_pair, rightup_point_pair, leftdown_point_pair]

    rightdown_point_pair = [
        [image_height, image_width],
        [
            image_height + expand_scale_list_list[3][1] * image_height,
            image_width + expand_scale_list_list[3][0] * image_width
        ]
    ]
    return [
        leftup_point_pair, rightup_point_pair, leftdown_point_pair,
        rightdown_point_pair
    ]


def getTransImage(image, trans_matrix):
    trans_image = np.zeros_like(image, dtype=np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            point = np.array([i, j, 1.0], dtype=np.float64).T
            trans_point = np.dot(trans_matrix, point).T
            trans_i = int(trans_point[0])
            if trans_i < 0 or trans_i >= image.shape[0]:
                continue
            trans_j = int(trans_point[1])
            if trans_j < 0 or trans_j >= image.shape[1]:
                continue
            trans_image[i, j] = image[trans_i, trans_j]
    return trans_image


def getBiggerImage(image, expand_scale_list_list, render=False, wait_key=0):
    image_height, image_width = image.shape[:2]

    sym_expand_scale_list_list = [
        expand_scale_list_list[0], expand_scale_list_list[1],
        expand_scale_list_list[1], expand_scale_list_list[0]
    ]

    point_pair_list = getBiggerPointPairList(image_width, image_height,
                                             sym_expand_scale_list_list)

    trans_matrix = getTransMatrix(point_pair_list)
    trans_matrix_inv = np.linalg.inv(trans_matrix)

    if render:
        renderTransImageBox(image, trans_matrix_inv, wait_key)

    return getTransImage(image, trans_matrix_inv)
