#!/usr/bin/env python
# -*- coding: utf-8 -*-

from texture_synthesis.Module.texture_generator import TextureGenerator


def demo():
    image_path = "./data/input1.jpg"
    block_size = 60
    num_block = 8
    mode = 'Best'  # Best or Cut
    print_progress = True

    texture_generator = TextureGenerator()
    image = texture_generator.generateTexture(image_path, block_size,
                                              (num_block, num_block), mode,
                                              print_progress)
    image.show()
    return True
