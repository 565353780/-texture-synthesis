#!/usr/bin/env python
# -*- coding: utf-8 -*-

from texture_synthesis.Demo.texture_generator import \
    demo as demo_generate_texture, \
    demo_repeat as demo_generate_repeat_texture, \
    demo_trans as demo_trans_image_to_texture, \
    demo_trans_folder as demo_trans_image_folder_to_texture, \
    demo_trans_all as demo_trans_image_to_all_texture, \
    demo_trans_folder_all as demo_trans_image_folder_to_all_texture

from texture_synthesis.Demo.texture_manager import \
    demo as demo_manage_texture

if __name__ == "__main__":
    #  demo_generate_texture()
    #  demo_generate_repeat_texture()
    #  demo_trans_image_to_texture()
    #  demo_trans_image_folder_to_texture()
    #  demo_trans_image_to_all_texture()

    demo_trans_image_folder_to_all_texture()
    demo_manage_texture()
