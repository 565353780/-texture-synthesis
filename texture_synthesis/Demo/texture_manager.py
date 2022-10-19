#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2

from texture_synthesis.Module.texture_manager import TextureManager


def demo():
    texture_file_path = "/home/chli/chLi/texture/Texture/flower/repeat.png"
    repeat_size = [3, 2]

    assert os.path.exists(texture_file_path)
    texture = cv2.imread(texture_file_path)

    texture_manager = TextureManager()
    repeat_texture = texture_manager.renderRepeatTexture(texture, repeat_size)

    cv2.imshow("repeat_texture", repeat_texture)
    cv2.waitKey(0)
    return True
