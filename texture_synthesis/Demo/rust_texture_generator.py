#!/usr/bin/env python
# -*- coding: utf-8 -*-

from texture_synthesis.Module.rust_texture_generator import RustTextureGenerator


def demo():
    image_file_path = "/home/chli/chLi/texture/Image/图片/11.jpg"
    save_texture_file_path = "/home/chli/chLi/texture/test.png"

    rust_texture_generator = RustTextureGenerator()
    rust_texture_generator.transImageToRepeatTexture(image_file_path,
                                                     save_texture_file_path)
    return True


def demo_folder():
    image_folder_path = "/home/chli/chLi/texture/Image/"
    save_texture_folder_path = "/home/chli/chLi/texture/RustTexture/"

    rust_texture_generator = RustTextureGenerator()
    rust_texture_generator.transImageFolderToRepeatTexture(
        image_folder_path, save_texture_folder_path)
    return True
