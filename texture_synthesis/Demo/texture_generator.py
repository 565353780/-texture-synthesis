#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2

from texture_synthesis.Module.texture_generator import TextureGenerator


def demo():
    image_file_path = "/home/chli/chLi/texture/图片/11.jpg"
    patch_sample_percent_list = [0.9, 0.9]
    patch_overlap_percent_list = [0.9, 0.9]
    block_num_list = [3, 3]
    print_progress = True

    assert os.path.exists(image_file_path)
    image = cv2.imread(image_file_path)

    texture_generator = TextureGenerator()
    generated_texture, image_shape, overlap = texture_generator.generateTexture(
        image, patch_sample_percent_list, patch_overlap_percent_list,
        block_num_list, print_progress)

    print("image_shape :", image_shape)
    print("overlap :", overlap)

    cv2.imshow("generated_texture", generated_texture)
    cv2.waitKey(0)
    return True


def demo_repeat():
    image_file_path = "/home/chli/chLi/texture/flower.png"

    assert os.path.exists(image_file_path)
    image = cv2.imread(image_file_path)

    texture_generator = TextureGenerator()
    width_repeat_texture = texture_generator.generateRepeatTexture(
        image, height_repeat=False)

    height_repeat_texture = texture_generator.generateRepeatTexture(
        image, width_repeat=False)

    repeat_texture = texture_generator.generateRepeatTexture(image)

    cv2.imshow("width_repeat_texture", width_repeat_texture)
    cv2.imshow("height_repeat_texture", height_repeat_texture)
    cv2.imshow("repeat_texture", repeat_texture)
    cv2.waitKey(0)
    return True


def demo_trans():
    image_file_path = "/home/chli/chLi/texture/Image/flower.png"
    save_texture_folder_path = "/home/chli/chLi/texture/Texture/flower/"
    width_repeat = True
    height_repeat = True

    texture_generator = TextureGenerator()
    texture_generator.transImageToRepeatTexture(image_file_path,
                                                save_texture_folder_path,
                                                width_repeat, height_repeat)
    return True


def demo_trans_folder():
    image_folder_path = "/home/chli/chLi/texture/Image/"
    save_texture_folder_path = "/home/chli/chLi/texture/Texture/"
    width_repeat = True
    height_repeat = True
    print_progress = True

    texture_generator = TextureGenerator()
    texture_generator.transImageFolderToRepeatTexture(
        image_folder_path, save_texture_folder_path, width_repeat,
        height_repeat, print_progress)
    return True


def demo_trans_all():
    image_file_path = "/home/chli/chLi/texture/Image/flower.png"
    save_texture_folder_path = "/home/chli/chLi/texture/Texture/flower/"

    texture_generator = TextureGenerator()
    texture_generator.transImageToAllRepeatTexture(image_file_path,
                                                   save_texture_folder_path)
    return True


def demo_trans_folder_all():
    image_folder_path = "/home/chli/chLi/texture/图片/"
    save_texture_folder_path = "/home/chli/chLi/texture/Texture/"
    print_progress = True

    texture_generator = TextureGenerator()
    texture_generator.transImageFolderToAllRepeatTexture(
        image_folder_path, save_texture_folder_path, print_progress)
    return True
