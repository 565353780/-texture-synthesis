#!/usr/bin/env python
# -*- coding: utf-8 -*-

# if call this package outside,
# then this 2 lines are needed for import the TextureGenerator module
'''
import sys
sys.path.append("path-to-the-folder-<texture_synthesis>")
'''

from texture_synthesis.Demo.texture_generator import \
    demo as demo_generate_repeat_texture, \
    demo_trans_folder_all as demo_trans_image_folder_to_all_texture
from texture_synthesis.Demo.render import demo as demo_render_repeat_texture
from texture_synthesis.Demo.image_cutter import demo as demo_cut_image
from texture_synthesis.Demo.sd_server import demo as demo_sd_server

if __name__ == "__main__":
    # demo coding for generating single texture for single image
    #  demo_generate_repeat_texture()

    # demo coding for translating images folder to repeat textures folder
    #  demo_trans_image_folder_to_all_texture()

    # demo coding for rendering the repeat texture
    #  demo_render_repeat_texture()

    # demo coding for cutting image and further running with sd
    demo_cut_image()

    # demo running stable diffusion server
    #  demo_sd_server()
