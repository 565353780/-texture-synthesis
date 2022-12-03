#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2

from texture_synthesis.Module.texture_generator import TextureGenerator


def demo():
    image_file_path = "/home/chli/chLi/texture/Image/图片/11.jpg"
    assert os.path.exists(image_file_path)
    image = cv2.imread(image_file_path)
    width_repeat = True
    height_repeat = True
    print_progress = True
    patch_sample_percent_list = [1.0, 1.0]
    patch_overlap_percent_list = [0.2, 0.2]
    scale_max_list = [0.5, 0.5, 0.5, 0.5]
    render_bigger_image = False
    wait_key = 0

    texture_generator = TextureGenerator()
    generated_texture = texture_generator.generateRepeatTexture(
        image, width_repeat, height_repeat, print_progress,
        patch_sample_percent_list, patch_overlap_percent_list, scale_max_list,
        render_bigger_image, wait_key)

    cv2.imshow("image", image)
    cv2.imshow("generated_texture", generated_texture)
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
    image_folder_path = "/home/chli/chLi/texture/Image/"
    save_texture_folder_path = "/home/chli/chLi/texture/Texture/"
    print_progress = True

    texture_generator = TextureGenerator()
    texture_generator.transImageFolderToAllRepeatTexture(
        image_folder_path, save_texture_folder_path, print_progress)
    return True
