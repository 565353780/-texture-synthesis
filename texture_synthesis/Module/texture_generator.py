#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import cv2

from texture_synthesis.Method.cut import getBlockImage
from texture_synthesis.Method.path import createFileFolder, renameFile
from texture_synthesis.Method.texture import generateBiggerTexture
from texture_synthesis.Module.texture_matcher import TextureMatcher
from texture_synthesis.Module.texture_optimizer import TextureOptimizer


class TextureGenerator(object):

    def __init__(self):
        self.texture_matcher = TextureMatcher()
        self.texture_optimizer = TextureOptimizer()
        return

    def generateRepeatTexture(self,
                              image,
                              width_repeat=True,
                              height_repeat=True,
                              print_progress=False,
                              patch_sample_percent_list=[1.0, 1.0],
                              patch_overlap_percent_list=[0.2, 0.2],
                              scale_max_list=[0.5, 0.5, 0.5, 0.5],
                              render_bigger_image=False,
                              wait_key=0):
        '''
        Input:
            image: np.ndarray
                source texture image
            width_repeat: bool
                whether repeat on width direction
            height_repeat: bool
                whether repeat on height direction
            print_progress: bool
                whether output the progress bar
            patch_sample_percent_list: [width_sample_percent,
                                        height_sample_percent]
                width_sample_percent: float, 0-1
                height_sample_percent: float, 0-1
                to compute the size of the patch in image,
                decide the final output texture size
            patch_overlap_percent_list: [width_overlap_percent,
                                         height_overlap_percent]
                width_overlap_percent: float, 0-1
                height_overlap_percent: float, 0-1
                decide both the final output texture size and the quality of the texture bound
                if it's bigger, the quality of the bound is higher,
                but the final output texture size is smaller
            scale_max_list: [leftup_width_scale_max,
                             leftup_height_scale_max,
                             rightup_width_scale_max,
                             rightup_height_scale_max]
                leftup_width_scale_max: float, 0-1
                leftup_height_scale_max: float, 0-1
                rightup_width_scale_max: float, 0-1
                rightup_height_scale_max: float, 0-1
                decide the transform search space,
                the corners of source image can randomly moving in this scale-bigger areas
            render_bigger_image: bool
                whether to render the optimized image by the best transform
            wait_key: int
                which key to wait for cv2
                0: wait until the user press Esc
                k * 1000: wait k seconds

            PS: the default params can adjust most images,
                change them only when the result is not excepted is recommended
        '''

        block_num_list = [1, 1],
        width_block_range = [0, 1]
        height_block_range = [0, 1]
        if width_repeat:
            block_num_list[0] = 3
            width_block_range = [1, 2]
        if height_repeat:
            block_num_list[1] = 3
            height_block_range = [1, 2]

        no_repeat_image = self.texture_matcher.matchRepeatTexture(
            image, patch_overlap_percent_list)

        best_scale_list = self.texture_optimizer.getBestScaleList(
            no_repeat_image, patch_sample_percent_list,
            patch_overlap_percent_list, block_num_list, scale_max_list,
            print_progress)

        texture, block_size, overlap, _ = generateBiggerTexture(
            no_repeat_image, patch_sample_percent_list,
            patch_overlap_percent_list, block_num_list, best_scale_list,
            render_bigger_image, wait_key, print_progress)

        #  cut = getBlockImage(texture, block_num_list, block_size, overlap,
        #  width_block_range, height_block_range)
        #  cv2.imshow("cut", cut)
        #  cv2.waitKey(5000)

        return getBlockImage(texture, block_num_list, block_size, overlap,
                             width_block_range, height_block_range)

    def transImageToRepeatTexture(self,
                                  image_file_path,
                                  save_texture_file_path,
                                  width_repeat=True,
                                  height_repeat=True,
                                  print_progress=False):
        assert os.path.exists(image_file_path)

        image = cv2.imread(image_file_path)

        texture = self.generateRepeatTexture(image, width_repeat,
                                             height_repeat, print_progress)

        createFileFolder(save_texture_file_path)

        cv2.imwrite(save_texture_file_path, texture)
        return True

    def transImageFolderToRepeatTexture(self,
                                        image_folder_path,
                                        save_texture_folder_path,
                                        width_repeat=True,
                                        height_repeat=True,
                                        print_progress=False):
        assert os.path.exists(image_folder_path)

        file_path_pair_list = []
        for root, _, files in os.walk(image_folder_path):
            current_save_texture_file_root_path = \
                root.replace(image_folder_path, save_texture_folder_path) + "/"
            for file_name in files:
                file_format = "." + file_name.split(".")[-1]
                if file_format not in [".jpg", ".jpeg", ".png"]:
                    continue

                image_file_path = root + "/" + file_name
                save_texture_file_path = current_save_texture_file_root_path + \
                    file_name[:-len(file_format)] + ".png"
                file_path_pair_list.append(
                    [image_file_path, save_texture_file_path])

        for i, file_path_pair in enumerate(file_path_pair_list):
            if print_progress:
                print(
                    "[INFO][TextureGenerator::transImageFolderToRepeatTexture]"
                )
                print("\t start trans image to repeat texture, " + str(i + 1) +
                      "/" + str(len(file_path_pair_list)) + "...")
            image_file_path, save_texture_file_path = file_path_pair

            if os.path.exists(save_texture_file_path):
                continue

            tmp_save_texture_file_path = save_texture_file_path[:-4] + "_tmp.png"

            self.transImageToRepeatTexture(image_file_path,
                                           tmp_save_texture_file_path,
                                           width_repeat, height_repeat,
                                           print_progress)

            renameFile(tmp_save_texture_file_path, save_texture_file_path)
        return True

    def transImageToAllRepeatTexture(self,
                                     image_file_path,
                                     save_texture_folder_path,
                                     print_progress=False):
        assert os.path.exists(image_file_path)

        image = cv2.imread(image_file_path)

        if print_progress:
            print("[INFO][TextureGenerator::transImageToAllRepeatTexture]")
            print("\t start trans image to width and height repeat texture...")
        repeat_texture = self.generateRepeatTexture(image, True, True,
                                                    print_progress)

        if print_progress:
            print("[INFO][TextureGenerator::transImageToAllRepeatTexture]")
            print("\t start trans image to width repeat texture...")
        width_repeat_texture = self.generateRepeatTexture(
            image, True, False, print_progress)

        if print_progress:
            print("[INFO][TextureGenerator::transImageToAllRepeatTexture]")
            print("\t start trans image to height repeat texture...")
        height_repeat_texture = self.generateRepeatTexture(
            image, False, True, print_progress)

        os.makedirs(save_texture_folder_path, exist_ok=True)

        cv2.imwrite(save_texture_folder_path + "repeat.png", repeat_texture)
        cv2.imwrite(save_texture_folder_path + "width_repeat.png",
                    width_repeat_texture)
        cv2.imwrite(save_texture_folder_path + "height_repeat.png",
                    height_repeat_texture)
        return True

    def transImageFolderToAllRepeatTexture(self,
                                           image_folder_path,
                                           save_texture_folder_path,
                                           print_progress=False):
        assert os.path.exists(image_folder_path)

        file_path_pair_list = []
        for root, _, files in os.walk(image_folder_path):
            current_save_texture_folder_root_path = \
                root.replace(image_folder_path, save_texture_folder_path) + "/"
            for file_name in files:
                file_format = "." + file_name.split(".")[-1]
                if file_format not in [".jpg", ".jpeg", ".png"]:
                    continue

                image_file_path = root + "/" + file_name
                current_save_texture_folder_path = \
                    current_save_texture_folder_root_path + file_name[:-len(file_format)] + "/"
                file_path_pair_list.append([
                    image_file_path,
                    current_save_texture_folder_path,
                ])

        for i, file_path_pair in enumerate(file_path_pair_list):
            if print_progress:
                print(
                    "[INFO][TextureGenerator::transImageFolderToRepeatTexture]"
                )
                print("\t start trans image to repeat texture, " + str(i + 1) +
                      "/" + str(len(file_path_pair_list)) + "...")
            image_file_path, current_save_texture_folder_path = file_path_pair

            if os.path.exists(current_save_texture_folder_path):
                continue

            tmp_save_texture_folder_path = current_save_texture_folder_path[:
                                                                            -1] + "_tmp/"

            self.transImageToAllRepeatTexture(image_file_path,
                                              tmp_save_texture_folder_path,
                                              print_progress)

            renameFile(current_save_texture_folder_path[:-1] + "_tmp/",
                       current_save_texture_folder_path)
        return True
