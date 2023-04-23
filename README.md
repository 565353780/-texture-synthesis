# Texture Synthesis

## Download

```bash
https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main
->./models/control_v11p_sd15_inpaint
https://huggingface.co/runwayml/stable-diffusion-v1-5/tree/main
->./models/v1-5-pruned.ckpt
```

## Install

### install rust

```bash
curl https://sh.rustup.rs -sSf | sh
```

and add

```bash
source $HOME/.cargo/env
```

to ~/.zshrc or ~/.bashrc

### prepare env

```bash
conda create -n texture python=3.8
conda activate texture
./setup.sh
```

## Run

```bash
python demo.py
```

## Run Control Stable Diffusion Server

```bash
python run_server.py
```

## Enjoy it~

