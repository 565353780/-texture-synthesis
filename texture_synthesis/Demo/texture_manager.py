#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2

from texture_synthesis.Module.texture_manager import TextureManager


def demo():
    texture_file_path = "/home/chli/chLi/texture/test.png"
    repeat_size = [3, 3]

    assert os.path.exists(texture_file_path)
    texture = cv2.imread(texture_file_path)

    texture_manager = TextureManager()
    repeat_texture = texture_manager.renderRepeatTexture(texture, repeat_size)

    cv2.imshow("repeat_texture", repeat_texture)
    cv2.waitKey(0)
    return True


def demo_folder():
    texture_folder_path = "/home/chli/chLi/texture/Texture/图片/11/"

    width_texture_file_path = texture_folder_path + "width_repeat.png"
    width_repeat_size = [3, 1]

    height_texture_file_path = texture_folder_path + "height_repeat.png"
    height_repeat_size = [1, 3]

    texture_file_path = texture_folder_path + "repeat.png"
    repeat_size = [3, 3]

    assert os.path.exists(texture_folder_path)
    width_texture = cv2.imread(width_texture_file_path)
    height_texture = cv2.imread(height_texture_file_path)
    texture = cv2.imread(texture_file_path)

    texture_manager = TextureManager()
    width_repeat_texture = texture_manager.renderRepeatTexture(
        width_texture, width_repeat_size)
    height_repeat_texture = texture_manager.renderRepeatTexture(
        height_texture, height_repeat_size)
    repeat_texture = texture_manager.renderRepeatTexture(texture, repeat_size)

    cv2.imshow("width_repeat_texture", width_repeat_texture)
    cv2.imshow("height_repeat_texture", height_repeat_texture)
    cv2.imshow("repeat_texture", repeat_texture)
    cv2.waitKey(0)
    return True
