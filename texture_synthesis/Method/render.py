#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import open3d as o3d


def renderMinCutPatch(dist_map):
    dist_array = dist_map.reshape(-1)

    dist_max = np.max(dist_array)
    points = []
    for i in range(dist_map.shape[0]):
        for j in range(dist_map.shape[1]):
            points.append([i, j, 1000 * dist_map[i][j]])
    points = np.array(points)
    colors = np.zeros_like(points)
    colors[:, 0] = dist_array / dist_max
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.visualization.draw_geometries([pcd])
    return True
