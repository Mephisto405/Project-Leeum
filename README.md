# Installation

1. Install COLMAP: https://colmap.github.io/install.html#linux
2. Install FFmpeg: https://jjeongil.tistory.com/1430
3. Install instant-ngp with **recursive** flag: https://github.com/NVlabs/instant-ngp#compilation-windows--linux
4. Install CMake: https://somjang.tistory.com/entry/Ubuntu-CMake-%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8-%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95
   1. `wget https://github.com/Kitware/CMake/releases/download/v3.23.2/cmake-3.23.2.tar.gz`
   2. `tar -xvf cmake-3.23.2.tar.gz`
   3. `rm cmake-3.23.2.tar.gz`
   4. `cd cmake-3.23.2`
   5. `apt-get install libssl-dev` # if 6 occurs error
   6. `./bootstrap`
   7. `make`
   8. `sudo make install`
5. Export paths:
   1. `vim ~/.bashrc` and add below at the end of the file.
      1. `export PATH="/usr/local/cuda{version}/bin:$PATH"`
      2. `export LD_LIBRARY_PATH="/usr/local/cuda{version}/lib64:$LD_LIBRARY_PATH"`
   2. `source ~/.bashrc` or restart the command line.
6. Turn off the Vulkan if Vulkan SDK is not yet installed. DLSS does not matter much.
   1. `cmake -DNGP_BUILD_WITH_VULKAN=OFF . -B build`
7. Reduce the number of job workers when `-j 16` occurs an error.
   1. `cmake --build build --config RelWithDebInfo -j 4`
8. `pip install commentjson`
9. `CUDA_VISIBLE_DEVICES=1 python ./scripts/run.py --mode nerf --scene ../data/dragonjar_half/`
   1. https://github.com/NVlabs/instant-ngp/issues/512
   2. imgs2imgs `CUDA_VISIBLE_DEVICES=1 python ./scripts/run.py --mode nerf --scene ../data/dragonjar_half/ --n_steps 5000 --screenshot_transforms ../data/dragonjar_half/transforms.json --screenshot_dir ../data/dragonjar_half/screenshot --width 304 --height 540`
   3. imgs2vid `ffmpeg -y -i ../data/dragonjar_half/screenshot/%04d.jpg -framerate 30 -c:v libx264 -pix_fmt yuv420p  ../data/dragonjar_half/screenshot.mp4`
   4. `CUDA_VISIBLE_DEVICES=1 python ./scripts/run.py --mode nerf --scene ../data/dragonjar_half/ --n_steps 5000 --save_mesh ../data/dragonjar_half/mesh.obj --screenshot_transforms ../data/dragonjar_half/transforms.json --screenshot_dir ../data/dragonjar_half/screenshot --width 304 --height 540 --screenshot_frames 0`
   5. `CUDA_VISIBLE_DEVICES=1 python ./scripts/run.py --mode nerf --scene ../data/black_half/ --save_mesh ../data/black_half/mesh.obj --save_snapshot ../data/black_half/mesh.obj`
   6. `CUDA_VISIBLE_DEVICES=1 python ./scripts/run.py --mode nerf --scene ../data/dragonjar_half/ --load_snapshot ../data/dragonjar_half/model.msgpack --screenshot_spiral --screenshot_dir ../data/dragonjar_half/screenshot --width 1080 --height 1920 --screenshot_frames 400`

# Video Resizing
`ffmpeg -i data/dragonjar.mp4 -vf scale=-1:540 -preset slow -crf 18 data/dragonjar_half.mp4`

# Data Processing via COLMAP
`python instant-ngp/scripts/colmap2nerf.py --video_in data/dragonjar_half/dragonjar_half.mp4 --video_fps 30 --run_colmap --aabb_scale 16`

# X Server Forwarding to using GUI and Saving Checkpoints
How to use XcXsrv with VSCode server: https://yunusmuhammad007.medium.com/jetson-nano-vs-code-x11-forwarding-over-ssh-d97fd2290973
How to download XcXsrv: https://sourceforge.net/projects/vcxsrv/
How to install XcXsrv: https://fossa.tistory.com/6