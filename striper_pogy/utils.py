import os
from collections import namedtuple
from typing import List, Tuple, Union

import numpy as np
from matplotlib import pyplot as plt

Size = namedtuple('Size', 'width height')
Location = namedtuple('Location', 'x y')
Populations = List[Tuple[Union[int, float], Union[int, float]]]

PLOTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plots'))
GAME_PATH = os.path.join(PLOTS_PATH, 'simulations')
EQUATIONS_PATH = os.path.join(PLOTS_PATH, 'equations')


def increment_filename(filename: str):
    """
    Checks to see if a file with the given filename exists.
    If so, keeps incrementing the number in the filename until the corresponding file does not exist.
    """
    while os.path.exists(filename):
        prefix = filename[:-4]  # remove file extension
        extension = filename[-4:]
        parts = prefix.split('::')  # split on :: to access the number in the filename
        number = int(parts[-1]) + 1  # increment file number
        filename = f'{parts[0]}::{number}{extension}'
    return filename


def limits(x: np.array) -> Tuple[int, int]:
    """ Intelligently determine the upper and lower limits of an axis in the plots."""
    max_x = max(x)
    factor = 1000 if max_x > 2000 else 100 if max_x > 200 else 10 if max_x > 20 else 2
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
    """
    Plots continuous lines from the given data.

    :param x: x-values to use for all curves.
    :param ys: List of arrays where each array stores the y-values of each curve.
    :param curve_colors: List of colors corresponding to each curve.
    :param curve_labels: List of labels corresponding to each curve.,.
    :param plot_size: dimensions of the plot to draw.
    :param dpi: resolution of the plot to draw.
    :param x_label: label to use for the x-axis.
    :param y_label: label to use for the y-axis.
    :param title: title to use for the plot.
    :param filename: path to the file where the plot is to be saved.
    """
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
        plt.plot(x, ys[i], c=curve_colors[i], label=curve_labels[i], lw=1)

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
    """
    Plots continuous lines from the given data.

    :param x: x-values of the curve.
    :param y: y-values of the curve.
    :param plot_size: dimensions of the plot to draw.
    :param dpi: resolution of the plot to draw.
    :param x_label: label to use for the x-axis.
    :param y_label: label to use for the y-axis.
    :param title: title to use for the plot.
    :param filename: path to the file where the plot is to be saved.
    """
    plt.clf()
    fig = plt.figure(figsize=plot_size, dpi=dpi)
    ax = fig.add_subplot(111)
    plt.quiver(x[:-1], y[:-1], x[1:] - x[:-1], y[1:] - y[:-1],
               scale_units='xy', angles='xy', scale=1, width=0.003)

    ax.set_xlim(limits(x))
    plt.xlabel(x_label)

    ax.set_ylim(limits(y))
    plt.ylabel(y_label)

    plt.title(title)

    plt.savefig(filename, bbox_inches='tight', pad_inches=0.25)
    plt.close('all')
    return
