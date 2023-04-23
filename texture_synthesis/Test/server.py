#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../ControlNet-v1-1-nightly')

from copy import deepcopy

import cv2
import torch
import einops
import random
import numpy as np
import gradio as gr
from pytorch_lightning import seed_everything

import config
from share import *
from annotator.util import resize_image, HWC3

from texture_synthesis.Module.image_cutter import ImageCutter


class Server(object):
    def __init__(self):
        self.image_cutter = None
        self.mask_cutter = None
        return

    def getMergedImageAndMask(self, input_image, input_mask, width_expand,
                              height_expand):
        self.image_cutter = ImageCutter(width_expand, height_expand)
        self.mask_cutter = ImageCutter(width_expand, height_expand)

        image_data = self.image_cutter.cutImage(input_image)
        mask_data = self.mask_cutter.cutImage(input_mask[:, :, 0])

        merged_image = image_data['merged_image']
        merged_mask = deepcopy(mask_data['merged_image'])
        image_mask = deepcopy(image_data['mask']).astype(np.uint8) * 255
        merged_mask[np.where(image_mask == 255)] = 255
        return merged_image, merged_mask

    def process(self, input_image_and_mask, prompt, a_prompt, n_prompt,
                num_samples, width_expand, height_expand, image_resolution,
                ddim_steps, guess_mode, strength, scale, seed, eta):

        with torch.no_grad():
            input_image = HWC3(input_image_and_mask['image'])
            input_mask = input_image_and_mask['mask']

            merged_image, merged_mask = self.getMergedImageAndMask(
                input_image, input_mask, width_expand, height_expand)

            img = resize_image(merged_image, image_resolution)
            H, W, C = img.shape

            detected_mask = cv2.resize(merged_mask, (W, H),
                                       interpolation=cv2.INTER_LINEAR)

            cv2.imwrite('/home/chli/chLi/input_image.png', input_image)
            cv2.imwrite('/home/chli/chLi/img.png', img)
            cv2.imwrite('/home/chli/chLi/detected_mask.png', detected_mask)
            return []

            detected_map = img.astype(np.float32).copy()
            detected_map[
                detected_mask > 127] = -255.0  # use -1 as inpaint value

            control = torch.from_numpy(
                detected_map.copy()).float().cuda() / 255.0
            control = torch.stack([control for _ in range(num_samples)], dim=0)
            control = einops.rearrange(control, 'b h w c -> b c h w').clone()

            if seed == -1:
                seed = random.randint(0, 65535)
            seed_everything(seed)

            cond = {
                "c_concat": [control],
            }
            un_cond = {
                "c_concat": None if guess_mode else [control],
            }
            shape = (4, H // 8, W // 8)
        return []

    def start(self):

        block = gr.Blocks().queue()
        with block:
            with gr.Row():
                gr.Markdown("## Control Stable Diffusion with Inpaint Mask")
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(source='upload',
                                           type="numpy",
                                           tool="sketch")
                    prompt = gr.Textbox(label="Prompt")
                    run_button = gr.Button(label="Run")
                    num_samples = gr.Slider(label="Images",
                                            minimum=1,
                                            maximum=12,
                                            value=1,
                                            step=1)
                    seed = gr.Slider(label="Seed",
                                     minimum=-1,
                                     maximum=2147483647,
                                     step=1,
                                     value=12345)
                    det = gr.Radio(choices=["None"],
                                   type="value",
                                   value="None",
                                   label="Preprocessor")
                    with gr.Accordion("Advanced options", open=False):
                        width_expand = gr.Slider(label="Width Expand",
                                                 minimum=0.0,
                                                 maximum=1.0,
                                                 value=0.1,
                                                 step=0.01)
                        height_expand = gr.Slider(label="Height Expand",
                                                  minimum=0.0,
                                                  maximum=1.0,
                                                  value=0.1,
                                                  step=0.01)
                        image_resolution = gr.Slider(label="Image Resolution",
                                                     minimum=256,
                                                     maximum=768,
                                                     value=512,
                                                     step=64)
                        strength = gr.Slider(label="Control Strength",
                                             minimum=0.0,
                                             maximum=2.0,
                                             value=1.0,
                                             step=0.01)
                        guess_mode = gr.Checkbox(label='Guess Mode',
                                                 value=False)
                        ddim_steps = gr.Slider(label="Steps",
                                               minimum=1,
                                               maximum=100,
                                               value=20,
                                               step=1)
                        scale = gr.Slider(label="Guidance Scale",
                                          minimum=0.1,
                                          maximum=30.0,
                                          value=9.0,
                                          step=0.1)
                        eta = gr.Slider(label="DDIM ETA",
                                        minimum=0.0,
                                        maximum=1.0,
                                        value=1.0,
                                        step=0.01)
                        a_prompt = gr.Textbox(label="Added Prompt",
                                              value='best quality')
                        n_prompt = gr.Textbox(
                            label="Negative Prompt",
                            value=
                            'lowres, bad anatomy, bad hands, cropped, worst quality'
                        )
                with gr.Column():
                    result_gallery = gr.Gallery(label='Output',
                                                show_label=False,
                                                elem_id="gallery").style(
                                                    grid=2, height='auto')
            ips = [
                input_image, prompt, a_prompt, n_prompt, num_samples,
                width_expand, height_expand, image_resolution, ddim_steps,
                guess_mode, strength, scale, seed, eta
            ]
            run_button.click(fn=self.process,
                             inputs=ips,
                             outputs=[result_gallery])

        block.launch(server_name='0.0.0.0', server_port=6007)
        return True


def test():
    server = Server()
    server.start()
    return True
