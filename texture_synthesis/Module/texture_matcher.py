#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from copy import deepcopy
from tqdm import tqdm, trange

from texture_synthesis.Data.patch import Patch
from texture_synthesis.Method.dist import getPatchImage, getPatchDistMatrixWithPool


class TextureMatcher(object):

    def __init__(self):
        self.sift = cv2.xfeatures2d.SIFT_create()

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)

        self.orb = cv2.ORB_create()
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        return

    def matchRepeatTextureBySIFT(self, image):
        kp1, des1 = self.sift.detectAndCompute(image, None)

        matches = self.flann.knnMatch(des1, des1, k=2)
        matches_mask = [[0, 0] for i in range(len(matches))]
        good = []

        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append([m])

        match_result = cv2.drawMatchesKnn(image,
                                          kp1,
                                          image,
                                          kp1,
                                          good,
                                          None,
                                          flags=2)

        cv2.imshow("match_result", match_result)
        cv2.waitKey(5000)
        return True

    def matchRepeatTextureByORB(self, image):
        _, image_width, _ = image.shape

        kp1, des1 = self.orb.detectAndCompute(image, None)

        matches = self.bf.match(des1, des1)
        matches = sorted(matches, key=lambda x: x.distance)

        knn_matches = self.bf.knnMatch(des1, des1, k=1)

        image_width = image.shape[1]

        remove_idx_list = []
        for i in range(len(matches) - 1):
            for j in range(i, len(matches)):
                m = matches[i]
                n = matches[j]
                if m.distance >= n.distance * 0.75:
                    remove_idx_list.append(i)
                    break
        print(remove_idx_list)

        match_result = cv2.drawMatches(image,
                                       kp1,
                                       image,
                                       kp1,
                                       matches,
                                       image,
                                       flags=2)

        keypoints = cv2.drawKeypoints(image, kp1, des1, color=(255, 0, 255))
        cv2.imshow("keypoints", keypoints)
        cv2.imshow("match_result", match_result)
        cv2.waitKey(5000)
        return True

    def matchRepeatTextureByORBCutImage(self, image):
        cut_num = 10

        image_height, image_width, _ = image.shape

        for i in range(1, cut_num):
            cut_x = int(image_width * i / cut_num)

            left_image = image[:, :cut_x]
            right_image = image[:, cut_x:]

            kp1, des1 = self.orb.detectAndCompute(left_image, None)
            kp2, des2 = self.orb.detectAndCompute(right_image, None)

            matches = self.bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)

            knn_matches = self.bf.knnMatch(des1, des2, k=1)

            image_width = image.shape[1]

            remove_idx_list = []
            for i in range(len(matches) - 1):
                for j in range(i, len(matches)):
                    m = matches[i]
                    n = matches[j]
                    if m.distance >= n.distance * 0.75:
                        remove_idx_list.append(i)
                        break
            print(remove_idx_list)

            match_result = cv2.drawMatches(left_image,
                                           kp1,
                                           right_image,
                                           kp2,
                                           matches,
                                           right_image,
                                           flags=2)

            keypoints = cv2.drawKeypoints(image,
                                          kp1,
                                          des1,
                                          color=(255, 0, 255))
            cv2.imshow("keypoints", keypoints)
            cv2.imshow("match_result", match_result)
            cv2.waitKey(5000)

        return True

    def matchRepeatTextureByPatchDist(self, image):
        search_patch_size_list = [100]

        image_height, image_width, _ = image.shape

        for search_patch_size in search_patch_size_list:
            patch_dist_matrix = getPatchDistMatrixWithPool(
                image, search_patch_size)

            min_dist_xy_idx = np.argmin(patch_dist_matrix)
            print(min_dist_xy_idx)
            exit()
        return True

    def matchRepeatTextureByTemplate(self, image):
        search_patch_size_list = [100]
        image_height, image_width, _ = image.shape

        for search_patch_size in search_patch_size_list:
            for x in range(image_width):
                for y in range(image_height):
                    patch_1 = Patch.fromList(
                        [[x, y],
                         [x + search_patch_size, y + search_patch_size]])
                    patch_image = getPatchImage(image, patch_1)
                    if patch_image is None:
                        continue

                    search_image = deepcopy(image)
                    search_image[y:y + search_patch_size,
                                 x:x + search_patch_size, :] = 0
                    print(search_image.shape)
                    print(patch_image.shape)

                    cv2.imshow("search_image", search_image)
                    cv2.imshow("patch_image", patch_image)
                    cv2.waitKey(5000)

                    result = cv2.matchTemplate(search_image, patch_image,
                                               cv2.TM_CCOEFF_NORMED)

                    cv2.imshow("template result", result)
                    cv2.waitKey(5000)
                    exit()
        return True

    def matchRepeatTexture(self, image):
        mode_list = ['sift', 'orb', 'orb_cut_image', 'patch_dist', 'template']
        mode = 'template'

        if mode == 'sift':
            return self.matchRepeatTextureBySIFT(image)
        if mode == 'orb':
            return self.matchRepeatTextureByORB(image)
        if mode == 'orb_cut_image':
            return self.matchRepeatTextureByORBCutImage(image)
        if mode == 'patch_dist':
            return self.matchRepeatTextureByPatchDist(image)
        if mode == 'template':
            return self.matchRepeatTextureByTemplate(image)
        return True
