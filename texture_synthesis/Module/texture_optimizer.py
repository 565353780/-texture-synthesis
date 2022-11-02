#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.optimize import minimize

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

    def generateBestTexture(self, image, patch_sample_percent_list,
                            patch_overlap_percent_list, block_num_list,
                            scale_max_list):
        self.loadImage(image, patch_sample_percent_list,
                       patch_overlap_percent_list, block_num_list)

        cons = {
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
        }

        init_scale_list = np.asarray([0.0, 0.0, 0.0, 0.0], dtype=np.float64)
        res = minimize(self.generateBiggerTexture,
                       init_scale_list,
                       constraints=cons)
        print(res.fun)
        print(res.success)
        print(res.x)
        exit()
        return res.x
