import os
from typing import Optional, List

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from board import Board
from utils import Measurements, increment_filename, PLOTS_PATH


def simulate(time_steps: int, gif_path: Optional[str] = None) -> Measurements:
    if time_steps < 1:
        raise ValueError(f'must simulate for at least one time step. Got {time_steps}')

    bay = Board()
    measurements: Measurements = list()
    images: List[Image] = list()

    for _ in range(time_steps):
        measurements.append(bay.step())
        if gif_path is not None:
            im = bay.draw()
            images.append(im)

    if gif_path is not None:
        gif_path = increment_filename(gif_path)
        images[0].save(
            gif_path,
            save_all=True,  # save all images in gif.
            optimize=True,  # reduces final filesize of the gif.
            append_images=images[1:],  # ordered list of other images.
            duration=1_500,  # each frame is shown of these many milliseconds.
        )
        pass

    return measurements


def draw_population_plot(measurements: Measurements, filename: str):
    filename = increment_filename(filename)
    plt.clf()

    x = np.arange(start=0, stop=len(measurements), dtype=int)
    y1 = np.asarray([m[0] for m in measurements], dtype=int)
    y2 = np.asarray([m[1] for m in measurements], dtype=int)

    fig = plt.figure(figsize=(9, 4.5), dpi=200)
    ax = fig.add_subplot(111)
    plt.plot(x, np.clip(y1, a_min=1, a_max=None), c='blue', label='pogies', lw=.8)
    plt.plot(x, np.clip(y2, a_min=1, a_max=None), c='red', label='stripers', lw=.8)

    x_lim = [0, len(x) + 1]
    ax.set_xlim(x_lim)
    plt.xticks(list(range(x_lim[0], x_lim[1], x_lim[1] // 10)))
    plt.xlabel('time')

    y_lim = [0, 10 * (1 + max(max(y1), max(y2)) // 10)]
    ax.set_ylim(y_lim)
    plt.yticks(list(range(y_lim[0], y_lim[1] + 1, 10)))
    plt.ylabel('population')

    plt.title(f'populations of stripers and menhaden against time')
    plt.legend(loc='upper left')

    plt.savefig(filename, bbox_inches='tight', pad_inches=0.25)
    plt.close('all')
    return


def draw_phase_plot(measurements: Measurements, filename: str):
    filename = increment_filename(filename)
    plt.clf()

    x = np.asarray([m[0] for m in measurements], dtype=int)
    y = np.asarray([m[1] for m in measurements], dtype=int)

    fig = plt.figure(figsize=(6, 6), dpi=200)
    ax = fig.add_subplot(111)
    plt.quiver(x[:-1], y[:-1], x[1:] - x[:-1], y[1:] - y[:-1],
               scale_units='xy', angles='xy', scale=1, width=0.003)

    x_lim = [-1, 10 * (1 + max(x) // 10)]
    ax.set_xlim(x_lim)
    plt.xticks(list(range(0, x_lim[1] + 1, 10)))
    plt.xlabel('pogies')

    y_lim = [-1, 2 * (1 + max(y) // 2)]
    ax.set_ylim(y_lim)
    plt.yticks(list(range(0, y_lim[1] + 1, 2)))
    plt.ylabel('stripers')

    plt.title(f'phase plot of striper population vs pogy population')

    plt.savefig(filename, bbox_inches='tight', pad_inches=0.25)
    plt.close('all')
    return


if __name__ == '__main__':
    np.random.seed(0)

    # Create plots directory (if needed) and remove any pre-existing files
    os.makedirs(PLOTS_PATH, exist_ok=True)
    for _root, _, _files in os.walk(PLOTS_PATH):
        [os.remove(os.path.join(_root, _file)) for _file in _files]

    # create directory for population vs time plots
    _population_path = os.path.join(PLOTS_PATH, 'population-vs-time')
    os.makedirs(_population_path, exist_ok=True)

    # create directory for phase plots
    _phase_path = os.path.join(PLOTS_PATH, 'phase-plots')
    os.makedirs(_phase_path, exist_ok=True)

    _gif_path = os.path.join(PLOTS_PATH, 'simulations')
    os.makedirs(_gif_path, exist_ok=True)

    for _i in range(1):
        if _i == 0:
            _measurements = simulate(time_steps=100, gif_path=os.path.join(_gif_path, 'simulation::0.gif'))
        else:
            _measurements = simulate(time_steps=100, gif_path=None)
        draw_population_plot(_measurements, os.path.join(_population_path, 'plot::0.png'))
        draw_phase_plot(_measurements, os.path.join(_phase_path, 'plot::0.png'))
