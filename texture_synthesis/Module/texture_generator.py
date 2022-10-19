#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import heapq
import numpy as np
from tqdm import tqdm


def randomPatch(texture, block_size):
    h, w, _ = texture.shape

    if h == block_size:
        i = 0
    else:
        i = np.random.randint(h - block_size)

    if w == block_size:
        j = 0
    else:
        j = np.random.randint(w - block_size)

    return texture[i:i + block_size, j:j + block_size]


def L2OverlapDiff(patch, block_size, overlap, result, y, x):
    error = 0
    if x > 0:
        left = patch[:, :overlap] - result[y:y + block_size, x:x + overlap]
        error += np.sum(left**2)

    if y > 0:
        up = patch[:overlap, :] - result[y:y + overlap, x:x + block_size]
        error += np.sum(up**2)

    if x > 0 and y > 0:
        corner = patch[:overlap, :overlap] - result[y:y + overlap,
                                                    x:x + overlap]
        error -= np.sum(corner**2)

    return error


def randomBestPatch(texture, block_size, overlap, result, y, x):
    h, w, _ = texture.shape
    errors = np.zeros((h - block_size, w - block_size))

    for i in range(h - block_size):
        for j in range(w - block_size):
            patch = texture[i:i + block_size, j:j + block_size]
            e = L2OverlapDiff(patch, block_size, overlap, result, y, x)
            errors[i, j] = e

    if errors.shape[0] > 0 and errors.shape[1] > 0:
        i, j = np.unravel_index(np.argmin(errors), errors.shape)
    else:
        i, j = 0, 0
    return texture[i:i + block_size, j:j + block_size]


def minCutPath(errors):
    # dijkstra's algorithm vertical
    pq = [(error, [i]) for i, error in enumerate(errors[0])]
    heapq.heapify(pq)

    h, w = errors.shape
    seen = set()

    while pq:
        error, path = heapq.heappop(pq)
        curDepth = len(path)
        curIndex = path[-1]

        if curDepth == h:
            return path

        for delta in -1, 0, 1:
            nextIndex = curIndex + delta

            if 0 <= nextIndex < w:
                if (curDepth, nextIndex) not in seen:
                    cumError = error + errors[curDepth, nextIndex]
                    heapq.heappush(pq, (cumError, path + [nextIndex]))
                    seen.add((curDepth, nextIndex))


def minCutPatch(patch, overlap, result, y, x):
    patch = patch.copy()
    dy, dx, _ = patch.shape
    minCut = np.zeros_like(patch, dtype=bool)

    if x > 0:
        left = patch[:, :overlap] - result[y:y + dy, x:x + overlap]
        leftL2 = np.sum(left**2, axis=2)
        for i, j in enumerate(minCutPath(leftL2)):
            minCut[i, :j] = True

    if y > 0:
        up = patch[:overlap, :] - result[y:y + overlap, x:x + dx]
        upL2 = np.sum(up**2, axis=2)
        for j, i in enumerate(minCutPath(upL2.T)):
            minCut[:i, j] = True

    np.copyto(patch, result[y:y + dy, x:x + dx], where=minCut)

    return patch


class TextureGenerator(object):

    def __init__(self):
        return

    def generateTexture(self,
                        image_path,
                        block_size,
                        num_block,
                        print_progress=False):
        assert os.path.exists(image_path)

        texture = cv2.imread(image_path)
        texture = texture / 255.0

        overlap = block_size // 6

        block_width_num, block_height_num = num_block

        w = (block_width_num * block_size) - (block_width_num - 1) * overlap
        h = (block_height_num * block_size) - (block_height_num - 1) * overlap
        print("image size:", w, h)

        result = np.zeros((h, w, texture.shape[2]))

        block_num = block_width_num * block_height_num

        for_data = range(block_num)
        if print_progress:
            print("[INFO][TextureGenerator::generateTexture]")
            print("\t start generate texture...")
            for_data = tqdm(for_data)
        for block_idx in for_data:
            width_idx = block_idx // block_height_num
            height_idx = block_idx % block_height_num

            x = width_idx * (block_size - overlap)
            y = height_idx * (block_size - overlap)

            if width_idx == 0 and height_idx == 0:
                patch = randomPatch(texture, block_size)
            else:
                patch = randomBestPatch(texture, block_size, overlap, result,
                                        y, x)
                patch = minCutPatch(patch, overlap, result, y, x)

            result[y:y + block_size, x:x + block_size] = patch

        image = (result * 255).astype(np.uint8)
        return image
