import ast
import io

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import numpy as np
from PIL import Image
from pathlib import Path
from tqdm import tqdm


def _plot_energy_axis(value, width):
    # range of energy values
    min_value = -70
    max_value = 0
    size = 24

    height = 0.3
    blank_bottom = 1
    blank_top = 1

    fig = plt.figure(figsize=(width, height + blank_bottom + blank_top))
    gs = fig.add_gridspec(3, 1, height_ratios=[blank_top, height, blank_bottom])

    ax = fig.add_subplot(gs[1])
    plt.tick_params(labelsize=size)

    # coloring
    cmap = LinearSegmentedColormap.from_list("custom_cmap", ["blue", "red"])
    norm = plt.Normalize(min_value, max_value)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    for i in range(min_value, max_value + 1):
        ax.axvspan(i, i + 1, color=cmap(norm(i)), zorder=-1)

    arrow_color = cmap(norm(value))
    ax.annotate(
        f"Energy: {value:.0f}",
        xy=(value, 1),
        xytext=(value, 3),
        arrowprops=dict(facecolor=arrow_color, shrink=0.05, width=8, headwidth=20),
        fontsize=size,
        ha="center",
        va="bottom",
        color=arrow_color,
    )

    ax.set_xlim(min_value, max_value)
    ax.set_xticks(np.arange(min_value, max_value + 1, 10))
    ax.set_yticks([])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax_blank_top = fig.add_subplot(gs[0])
    ax_blank_top.axis("off")

    ax_blank_bottom = fig.add_subplot(gs[2])
    ax_blank_bottom.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    plt.close(fig)
    image = Image.open(buf)

    return image


def _cat_energy_plot(frame, energy):

    frame_width, _ = frame.size
    eplot = _plot_energy_axis(energy, width=frame_width / 100)

    new_height = frame.height + eplot.height
    new_image = Image.new("RGB", (frame_width, new_height))

    new_image.paste(frame, (0, 0))
    new_image.paste(eplot, (0, frame.height))

    return new_image


def append_energy(frames: Path, freeenergy_file: Path):
    with open(freeenergy_file, "r") as f:
        # energies looks like '[1, 2, 3, ..., 100]' with length of 100
        energies = f.readline()
        energies = ast.literal_eval(energies)
    for i, energy in enumerate(tqdm(energies, desc="Appending energy to frames")):
        frame = Image.open(frames / f"frame_{i}.png")
        combined_image = _cat_energy_plot(frame, energy)
        Path(frames / "with_energy").mkdir(exist_ok=True)
        combined_image.save(frames / "with_energy" / f"frame_w_energy_{i}.png")


if __name__ == "__main__":
    initial_frame = Image.open("../frames/1213test/frame_0.png")

    combined_image = _cat_energy_plot(initial_frame, energy=-35.1222)
    combined_image.show()
