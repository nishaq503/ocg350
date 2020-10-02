import os

import numpy as np
from matplotlib import pyplot as plt

from board import Board
from utils import Measurements, increment_filename, PLOTS_PATH

CANVAS_MULTIPLIER = 6


def simulate(time_steps: int) -> Measurements:
    if time_steps < 1:
        raise ValueError(f'must simulate for at least one time step. Got {time_steps}')

    bay = Board()
    measurements: Measurements = list()

    measurements.append(bay.start(num_prey=3, num_predators=1))
    for _ in range(time_steps - 1):
        measurements.append(bay.step())

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

    # Create and plots directory (if needed) and remove are pre-existing files
    os.makedirs(PLOTS_PATH, exist_ok=True)
    for _root, _, _files in os.walk(PLOTS_PATH):
        [os.remove(os.path.join(_root, _file)) for _file in _files]
    _population_path = os.path.join(PLOTS_PATH, 'population-vs-time')
    _phase_path = os.path.join(PLOTS_PATH, 'phase-plots')
    os.makedirs(_population_path, exist_ok=True)
    os.makedirs(_phase_path, exist_ok=True)

    for _ in range(10):
        _measurements = simulate(time_steps=100)
        draw_population_plot(_measurements, os.path.join(_population_path, 'plot::0.png'))
        draw_phase_plot(_measurements, os.path.join(_phase_path, 'plot::0.png'))
