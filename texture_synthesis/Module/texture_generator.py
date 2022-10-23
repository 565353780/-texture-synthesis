#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import cv2
import numpy as np
from tqdm import tqdm

from texture_synthesis.Method.cut import getBlockImage
from texture_synthesis.Method.patch import (getMinCutPatch, getRandomBestPatch,
                                            getRandomPatch)
from texture_synthesis.Method.path import createFileFolder, renameFile


class TextureGenerator(object):

    def __init__(self):
        return

    def generateTexture(self,
                        image,
                        patch_sample_percent_list,
                        patch_overlap_percent_list,
                        block_num_list,
                        print_progress=False):
        texture = image / 255.0

        block_size = [
            int(texture.shape[1 - i] * patch_sample_percent_list[i])
            for i in range(2)
        ]

        overlap = [
            int(block_size[i] * patch_overlap_percent_list[i])
            for i in range(2)
        ]

        block_width_num, block_height_num = block_num_list

        w = (block_width_num *
             block_size[0]) - (block_width_num - 1) * overlap[0]
        h = (block_height_num *
             block_size[1]) - (block_height_num - 1) * overlap[1]

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

            x = width_idx * (block_size[0] - overlap[0])
            y = height_idx * (block_size[1] - overlap[1])

            if width_idx == 0 and height_idx == 0:
                patch = getRandomPatch(texture, block_size)
            else:
                patch = getRandomBestPatch(texture, block_size, overlap,
                                           result, y, x)
                patch = getMinCutPatch(patch, overlap, result, y, x)

            result[y:y + block_size[1], x:x + block_size[0]] = patch

        generated_texture = (result * 255).astype(np.uint8)
        return generated_texture, block_size, overlap

    def generateRepeatTexture(self,
                              image,
                              width_repeat=True,
                              height_repeat=True,
                              print_progress=False):
        if not width_repeat and not height_repeat:
            return image

        pre_patch_sample_percent_list = [0.8, 0.8]
        pre_patch_overlap_percent_list = [0.9, 0.9]
        pre_block_num_list = [2, 2]

        pre_texture, _, _ = self.generateTexture(
            image, pre_patch_sample_percent_list,
            pre_patch_overlap_percent_list, pre_block_num_list, print_progress)

        #  cv2.imshow("pre_texture", pre_texture)
        #  cv2.waitKey(5000)

        patch_sample_percent_list = [1.0, 1.0]
        patch_overlap_percent_list = [0.2, 0.2]
        block_num_list = [1, 1]
        width_block_range = [0, 1]
        height_block_range = [0, 1]

        if width_repeat:
            block_num_list[0] = 3
            width_block_range = [1, 2]

        if height_repeat:
            block_num_list[1] = 3
            height_block_range = [1, 2]

        texture, block_size, overlap = self.generateTexture(
            pre_texture, patch_sample_percent_list, patch_overlap_percent_list,
            block_num_list, print_progress)

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

        for_data = file_path_pair_list
        if print_progress:
            print("[INFO][TextureGenerator::transImageFolderToRepeatTexture]")
            print("\t start trans image to repeat texture...")
            for_data = tqdm(file_path_pair_list)
        for file_path_pair in for_data:
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

        repeat_texture = self.generateRepeatTexture(image, True, True,
                                                    print_progress)
        width_repeat_texture = self.generateRepeatTexture(
            image, True, False, print_progress)
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

        for_data = file_path_pair_list
        if print_progress:
            print("[INFO][TextureGenerator::transImageFolderToRepeatTexture]")
            print("\t start trans image to repeat texture...")
            for_data = tqdm(file_path_pair_list)
        for file_path_pair in for_data:
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
