import os
from typing import List, Tuple, Union
from matplotlib import pyplot as plt

import numpy as np
from collections import namedtuple

GAME_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plots-game'))
EQUATIONS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plots-equations'))

Size = namedtuple('Size', 'width height')
Location = namedtuple('Location', 'x y')
Populations = List[Tuple[Union[int, float], Union[int, float]]]


def increment_filename(filename: str):
    while os.path.exists(filename):
        prefix = filename[:-4]  # remove file extension
        extension = filename[-4:]
        parts = prefix.split('::')
        number = int(parts[-1]) + 1  # increment plot number
        filename = f'{parts[0]}::{number}{extension}'
    return filename


def limits(x: np.array) -> Tuple[int, int]:
    factor = 100 if max(x) > 200 else 10 if max(x) > 20 else 2
    return min(x) - 1, min(x) + factor * (1 + (max(x) - min(x)) // factor)


def line_plot(
        x: np.array,
        ys: List[np.array],
        curve_colors: List[str],
        curve_labels: List[str],
        plot_size: Tuple[int, int],
        dpi: int,
        x_label: str,
        y_label: str,
        title: str,
        filename: str,
):
    if len(ys) != len(curve_colors):
        raise ValueError(f'must have a color for each curve. Got {len(ys)} curves but {len(curve_colors)} colors.')
    if len(ys) != len(curve_labels):
        raise ValueError(f'must have a label for each curve. Got {len(ys)} curves but {len(curve_labels)} labels.')
    if not all((len(y) == len(x) for y in ys)):
        raise ValueError(f'All curves must be of the same length as the x-axis.')

    plt.clf()
    fig = plt.figure(figsize=plot_size, dpi=dpi)
    ax = fig.add_subplot(111)
    for i in range(len(curve_colors)):
        plt.plot(x, ys[i], c=curve_colors[i], label=curve_labels[i], lw=0.8)

    ax.set_xlim(limits(x))
    plt.xlabel(x_label)

    y_lim = min([min(y) for y in ys]), max([max(y) for y in ys])
    ax.set_ylim(limits(y_lim))
    plt.ylabel(y_label)

    plt.title(title)
    plt.legend()
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.25)
    plt.close('all')
    return


def arrow_plot(
        x: np.array,
        y: np.array,
        plot_size: Tuple[int, int],
        dpi: int,
        x_label: str,
        y_label: str,
        title: str,
        filename: str,
):
    plt.clf()
    fig = plt.figure(figsize=plot_size, dpi=dpi)
    ax = fig.add_subplot(111)
    plt.quiver(x[:-1], y[:-1], x[1:] - x[:-1], y[1:] - y[:-1],
               scale_units='xy', angles='xy', scale=1, width=0.005)

    ax.set_xlim(limits(x))
    plt.xlabel(x_label)

    ax.set_ylim(limits(y))
    plt.ylabel(y_label)

    plt.title(title)

    plt.savefig(filename, bbox_inches='tight', pad_inches=0.25)
    plt.close('all')
    return


# Parameters that can be tweaked
SIZE_MULTIPLIER = 5  # 1.5
BOARD_SIZE: Size = Size(17 * SIZE_MULTIPLIER, 11 * SIZE_MULTIPLIER)
CANVAS_SCALE = (2 ** 11) // max(BOARD_SIZE)

PREY_SIZE: Size = Size(1, 1)  # 1.5
PREY_CAPACITY: int = 75 * (SIZE_MULTIPLIER ** 2)
# PREY_CAPACITY: int = 75  # 100
PREY_REPRODUCTION_RATE: float = 0.5  # .25

PREDATOR_SIZE: Size = Size(2.5, 2.5)  # 4
PREDATOR_FOOD_REQUIREMENTS: int = 3  # 2


def predator_reproduction_function(num_eaten: int) -> int:
    return num_eaten // PREDATOR_FOOD_REQUIREMENTS


def prey_reproduction_function(reproduction_rate: float) -> int:
    return 2 if np.random.uniform() < reproduction_rate else 1
