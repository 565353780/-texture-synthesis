#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from texture_synthesis.Module.texture_matcher import TextureMatcher

def demo():
    texture_file_path = "/home/chli/chLi/texture/Image/texture_1.jpg"

    texture_matcher = TextureMatcher()

    image = cv2.imread(texture_file_path)
    texture_matcher.matchRepeatTexture(image)
    return True
