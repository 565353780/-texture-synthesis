#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import open3d as o3d
from copy import deepcopy


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
