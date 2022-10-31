#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def getPointMatrix(point_array):
    point_matrix = np.ones((3, point_array.shape[0]), dtype=np.float64)
    for i in range(point_array.shape[0]):
        point_matrix[:2, i] = point_array[i]
    return point_matrix


def getTransMatrix(point_pair_list):
    point_pair_array = np.array(point_pair_list, dtype=np.float64)
    source_point_array = point_pair_array[:, 0]
    target_point_array = point_pair_array[:, 1]

    source_point_matrix = getPointMatrix(source_point_array)
    target_point_matrix = getPointMatrix(target_point_array)

    source_matrix = np.dot(source_point_matrix, source_point_matrix.T)
    target_matrix = np.dot(source_point_matrix, target_point_matrix.T)

    transpose_matrix = np.dot(np.linalg.inv(source_matrix), target_matrix)
    trans_matrix = transpose_matrix.T
    return trans_matrix
