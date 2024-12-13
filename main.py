from pathlib import Path
import argparse
from datetime import datetime

from render import render
from vis_energy import append_energy
from gif import generate_gif, optimize_gif

today = datetime.now().strftime('%m%d')

parser = argparse.ArgumentParser()
parser.add_argument('--version', type=str, default=f'{today}test')
parser.add_argument('--proj', type=str, default=r'D:\Libs\Desktop\P-L Binding\proj')
parser.add_argument('--complex', type=str, default='5H6V')

# render settings
parser.add_argument('--width', type=int, default=800)
parser.add_argument('--height', type=int, default=800)
parser.add_argument('--ray', type=int, default=0)
parser.add_argument('--dpi', type=int, default=150)
parser.add_argument('--antialias', action='store_true')

args = parser.parse_args()

def main():
    version = args.version
    output_filename = f'{version}.gif'

    proj_path = Path(args.proj)
    frames_path = proj_path / 'frames' / version
    GIF_path = proj_path / 'GIFs' / output_filename
    energyfile_path = proj_path / '5H6V-freeenergy.txt'

    render(args, frames_path)
    print(f'Frames saved to {frames_path}')

    append_energy(frames_path, energyfile_path)
    generate_gif(frames_path / 'with_energy', GIF_path)
    optimize_gif(GIF_path)

    print(f'GIF saved to {GIF_path}')

if __name__ == '__main__':
    main()