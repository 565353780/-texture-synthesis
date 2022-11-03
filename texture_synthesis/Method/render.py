#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from copy import deepcopy

import cv2
import numpy as np
import open3d as o3d

from texture_synthesis.Method.path import createFileFolder


def renderMinCutPatch(dist_map):
    dist_max = np.max(dist_map)
    dist_map = np.clip(dist_map, 0, dist_max / 4.0)

    dist_max = np.max(dist_map)
    dist_array = dist_map.reshape(-1)

    points = []
    for i in range(dist_map.shape[0]):
        for j in range(dist_map.shape[1]):
            points.append([i, j, 1000 * dist_map[i][j]])
    points = np.array(points)

    colors = np.zeros_like(points)
    colors[:, 0] = dist_array / dist_max
    colors[:, 2] = 1 - (dist_array / dist_max)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.visualization.draw_geometries([pcd])
    return True


def getRepeatedTexture(texture, repeat_size, scale=1.0):
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

    cv2.rectangle(repeat_texture, (0, 0), (texture_shape[1], texture_shape[0]),
                  (0, 255, 0), 2)

    if scale != 1.0:
        repeat_texture = cv2.resize(repeat_texture, None, fx=scale, fy=scale)
    return repeat_texture


def renderRepeatedTexture(image_file_path, repeat_size,
                          save_repeated_texture_file_path):
    assert os.path.exists(image_file_path)

    texture = cv2.imread(image_file_path)

    repeated_texture = getRepeatedTexture(texture, repeat_size)

    createFileFolder(save_repeated_texture_file_path)
    cv2.imwrite(save_repeated_texture_file_path, repeated_texture)
    return True


def renderTransImageBox(image, trans_matrix_inv, wait_key=0):
    render_image = deepcopy(image)
    point_list = np.array([
        [0, 0, 1],
        [0, render_image.shape[1], 1],
        [render_image.shape[0], 0, 1],
        [render_image.shape[0], render_image.shape[1], 1],
    ]).T
    trans_points = np.dot(trans_matrix_inv, point_list).T[:, [1, 0]]
    trans_points = trans_points[[0, 1, 3, 2]].reshape(1, -1, 2).astype(int)
    cv2.polylines(render_image, trans_points, True, [0, 255, 0])
    cv2.imshow("TransImageBox", render_image)
    cv2.waitKey(wait_key)
    return True
