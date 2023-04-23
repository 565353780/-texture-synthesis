cd ..
git clone https://github.com/EmbarkStudios/texture-synthesis.git rust-texture-synthesis
git clone https://github.com/lllyasviel/ControlNet-v1-1-nightly.git

pip install numpy opencv-python tqdm open3d

pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 \
  --extra-index-url https://download.pytorch.org/whl/cu116

cd texture-synthesis
pip install -r requirements.txt
