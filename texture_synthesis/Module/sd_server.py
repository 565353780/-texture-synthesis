#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import torch
import einops
import random
import numpy as np
import gradio as gr
from copy import deepcopy
from pytorch_lightning import seed_everything

import config
from share import *
from annotator.util import resize_image, HWC3
from cldm.model import create_model, load_state_dict
from cldm.ddim_hacked import DDIMSampler

from texture_synthesis.Module.image_cutter import ImageCutter


class SDServer(object):
    def __init__(self):
        self.model_name = 'control_v11p_sd15_inpaint'
        self.model = create_model(
            f'../ControlNet-v1-1-nightly/models/{self.model_name}.yaml').cpu()
        self.model.load_state_dict(load_state_dict(
            '../ControlNet-v1-1-nightly/models/v1-5-pruned.ckpt',
            location='cuda'),
                                   strict=False)
        self.model.load_state_dict(load_state_dict(
            f'../ControlNet-v1-1-nightly/models/{self.model_name}.pth',
            location='cuda'),
                                   strict=False)
        self.model = self.model.cuda()
        self.ddim_sampler = DDIMSampler(self.model)

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
        return merged_image, merged_mask, image_data

    def getRecombinedImage(self, image_data, image):
        merged_image_width, merged_image_height = image_data[
            'merged_image'].shape[:2]

        image_data['complete_merged_image'] = cv2.resize(
            deepcopy(image), (merged_image_height, merged_image_width))

        image_data = self.image_cutter.recombineImage(image_data)

        recombined_image = deepcopy(image_data['recombined_image'])
        return recombined_image

    def process(self, input_image_and_mask, prompt, a_prompt, n_prompt,
                num_samples, width_expand, height_expand, image_resolution,
                ddim_steps, guess_mode, strength, scale, seed, eta):

        with torch.no_grad():
            input_image = HWC3(input_image_and_mask['image'])
            input_mask = input_image_and_mask['mask']

            merged_image, merged_mask, image_data = self.getMergedImageAndMask(
                input_image, input_mask, width_expand, height_expand)

            img = resize_image(merged_image, image_resolution)
            H, W, C = img.shape

            detected_mask = cv2.resize(merged_mask, (W, H),
                                       interpolation=cv2.INTER_LINEAR)
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

            if config.save_memory:
                self.model.low_vram_shift(is_diffusing=False)

            cond = {
                "c_concat": [control],
                "c_crossattn": [
                    self.model.get_learned_conditioning(
                        [prompt + ', ' + a_prompt] * num_samples)
                ]
            }
            un_cond = {
                "c_concat":
                None if guess_mode else [control],
                "c_crossattn": [
                    self.model.get_learned_conditioning([n_prompt] *
                                                        num_samples)
                ]
            }
            shape = (4, H // 8, W // 8)

            if config.save_memory:
                self.model.low_vram_shift(is_diffusing=True)

            self.model.control_scales = [
                strength * (0.825**float(12 - i)) for i in range(13)
            ] if guess_mode else ([strength] * 13)
            # Magic number. IDK why. Perhaps because 0.825**12<0.01 but 0.826**12>0.01

            samples, intermediates = self.ddim_sampler.sample(
                ddim_steps,
                num_samples,
                shape,
                cond,
                verbose=False,
                eta=eta,
                unconditional_guidance_scale=scale,
                unconditional_conditioning=un_cond)

            if config.save_memory:
                self.model.low_vram_shift(is_diffusing=False)

            x_samples = self.model.decode_first_stage(samples)
            x_samples = (
                einops.rearrange(x_samples, 'b c h w -> b h w c') * 127.5 +
                127.5).cpu().numpy().clip(0, 255).astype(np.uint8)

            image_width, image_height = image_data['image'].shape[:2]

            masked_image = detected_map.clip(0, 255).astype(np.uint8)
            results = [x_samples[i] for i in range(num_samples)]

            new_masked_image = self.getRecombinedImage(image_data,
                                                       masked_image)

            return_image_list = [
                cv2.resize(new_masked_image, (image_height, image_width))
            ]
            for result in results:
                new_result = self.getRecombinedImage(image_data, result)
                return_image_list.append(
                    cv2.resize(new_result, (image_height, image_width)))

        return return_image_list

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

        block.launch(server_name='0.0.0.0', server_port=6006)
        return True
