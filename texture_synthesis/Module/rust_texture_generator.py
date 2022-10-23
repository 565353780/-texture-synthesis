#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm

from texture_synthesis.Method.path import createFileFolder, renameFile
from texture_synthesis.Method.cmd import runCMD


class RustTextureGenerator(object):

    def __init__(self):
        return

    def transImageToRepeatTexture(self,
                                  image_file_path,
                                  save_texture_file_path,
                                  resolution=400):
        assert os.path.exists(image_file_path)

        createFileFolder(save_texture_file_path)

        cmd = "cd ../rust-texture-synthesis && " + \
            "cargo run --release --" + \
            " --inpaint " + image_file_path + \
            " --out-size " + str(resolution) + \
            " --tiling -o " + save_texture_file_path + \
            " generate " + image_file_path

        assert runCMD(cmd)
        return True

    def transImageFolderToRepeatTexture(self,
                                        image_folder_path,
                                        save_texture_folder_path,
                                        resolution=400,
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
            print(
                "[INFO][RustTextureGenerator::transImageFolderToRepeatTexture]"
            )
            print("\t start trans image to repeat texture...")
            for_data = tqdm(file_path_pair_list)
        for file_path_pair in for_data:
            image_file_path, save_texture_file_path = file_path_pair

            if os.path.exists(save_texture_file_path):
                continue

            tmp_save_texture_file_path = save_texture_file_path[:-4] + "_tmp.png"

            self.transImageToRepeatTexture(image_file_path,
                                           tmp_save_texture_file_path,
                                           resolution)

            renameFile(tmp_save_texture_file_path, save_texture_file_path)
        return True
