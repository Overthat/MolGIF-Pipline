import imageio.v3 as iio
from pathlib import Path
import os
import subprocess

def generate_gif(frames_path, output_path):
    extract_number = lambda name: int(name.stem.split('_')[-1])
    file_names = sorted([Path(fn) for fn in frames_path.glob('*.png')], key=extract_number)
    frames = []
    for file_name in file_names:
        frame = iio.imread(file_name)
        frames.append(frame)
    print(f'Loaded {len(frames)} frames in folder {frames_path}')

    print('Generating GIF...')
    iio.imwrite(output_path, frames, format='gif', fps=10, loop=0)

def optimize_gif(output_path):
    additional_path = r"C:\Programs\CLI\gifsicle-1.95-win64"
    old_path = os.environ.get('PATH', '')
    os.environ['PATH'] = f"{additional_path};{old_path}"

    print('Optimizing GIF...')
    command = ['gifsicle', '-b', '-O2', '--colors=256', '--resize', '500x_', output_path]
    subprocess.run(command, check=True)