#!/usr/bin/env python
# -*- coding: utf-8 -*-

from texture_synthesis.Method.render import renderRepeatedTexture


def demo():
    repeat_texture_folder_path = "/home/chli/chLi/texture/Texture/"
    repeat_texture_file_relate_path_dict = {
        '0': 'texture/texture_1/repeat.png',
        '1': '木纹/22-02木纹09/repeat.png',
        '2': '木纹/22-02木纹10/repeat.png',
        '3': '木纹/22-02木纹12/repeat.png',
        '4': '木纹/北美黑胡桃/repeat.png',
    }

    render_file_idx = 4
    repeat_size = [3, 3]
    scale = 0.5
    wait_key = 0

    repeat_texture_file_path = \
        repeat_texture_folder_path + \
        repeat_texture_file_relate_path_dict[str(render_file_idx)]

    renderRepeatedTexture(repeat_texture_file_path, repeat_size, scale,
                          wait_key)
    return True
