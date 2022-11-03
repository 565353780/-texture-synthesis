#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from tqdm import tqdm
from scipy.optimize import minimize
from multiprocessing import Pool

from texture_synthesis.Method.texture import generateBiggerTexture


class TextureOptimizer(object):

    def __init__(self):
        self.image = None
        self.patch_sample_percent_list = None
        self.patch_overlap_percent_list = None
        self.block_num_list = None
        return

    def reset(self):
        self.image = None
        self.patch_sample_percent_list = None
        self.patch_overlap_percent_list = None
        self.block_num_list = None
        return True

    def loadImage(self, image, patch_sample_percent_list,
                  patch_overlap_percent_list, block_num_list):
        self.reset()

        self.image = image
        self.patch_sample_percent_list = patch_sample_percent_list
        self.patch_overlap_percent_list = patch_overlap_percent_list
        self.block_num_list = block_num_list
        return True

    def generateBiggerTexture(self, scale_list):
        _, _, _, error_sum = generateBiggerTexture(
            self.image, self.patch_sample_percent_list,
            self.patch_overlap_percent_list, self.block_num_list, scale_list)
        return error_sum

    def getBestScaleListByScipy(self, scale_max_list):
        cons = (
            {
                'type': 'ineq',
                'fun': lambda x: x[0]
            },
            {
                'type': 'ineq',
                'fun': lambda x: x[1]
            },
            {
                'type': 'ineq',
                'fun': lambda x: x[2]
            },
            {
                'type': 'ineq',
                'fun': lambda x: x[3]
            },
            {
                'type': 'ineq',
                'fun': lambda x: scale_max_list[0] - x[0]
            },
            {
                'type': 'ineq',
                'fun': lambda x: scale_max_list[1] - x[1]
            },
            {
                'type': 'ineq',
                'fun': lambda x: scale_max_list[2] - x[2]
            },
            {
                'type': 'ineq',
                'fun': lambda x: scale_max_list[3] - x[3]
            },
        )

        init_scale_list = np.asarray(scale_max_list, dtype=np.float64) / 2.0
        res = minimize(self.generateBiggerTexture,
                       init_scale_list,
                       method='SLSQP',
                       constraints=cons)
        if not res.success:
            print("[ERROR][TextureOptimizer::getBestScaleListByScipy]")
            print("\t minimize failed! return zero scale list!")
            return [0.0, 0.0, 0.0, 0.0]
        return res.x

    def getBestScaleListBySample(self,
                                 scale_max_list,
                                 sample_num,
                                 print_progress=False):
        assert sample_num > 0

        if sample_num == 1:
            return [0.0, 0.0, 0.0, 0.0]

        sample_scale_list_list = []
        for i in range(sample_num):
            for j in range(sample_num):
                for k in range(sample_num):
                    for l in range(sample_num):
                        sample_scale_list_list.append([
                            1.0 * scale_max_list[0] * i / (sample_num - 1),
                            1.0 * scale_max_list[1] * j / (sample_num - 1),
                            1.0 * scale_max_list[2] * k / (sample_num - 1),
                            1.0 * scale_max_list[3] * l / (sample_num - 1)
                        ])

        with Pool(os.cpu_count()) as pool:
            if print_progress:
                print("[INFO][TextureOptimizer::getBestScaleListBySample]")
                print("\t start sample scale list...")
                result = list(
                    tqdm(pool.imap(self.generateBiggerTexture,
                                   sample_scale_list_list),
                         total=len(sample_scale_list_list)))
            else:
                result = list(
                    pool.imap(self.generateBiggerTexture,
                              sample_scale_list_list))

        min_error_sample_scale_idx = np.argmin(result)
        return sample_scale_list_list[min_error_sample_scale_idx]

    def getBestScaleList(self,
                         image,
                         patch_sample_percent_list,
                         patch_overlap_percent_list,
                         block_num_list,
                         scale_max_list,
                         print_progress=False):
        mode_list = ['scipy', 'sample']
        mode = 'sample'

        assert mode in mode_list

        self.loadImage(image, patch_sample_percent_list,
                       patch_overlap_percent_list, block_num_list)

        if mode == 'scipy':
            return self.getBestScaleListByScipy(scale_max_list)
        if mode == 'sample':
            sample_num = 4
            return self.getBestScaleListBySample(scale_max_list, sample_num,
                                                 print_progress)
