import os
from collections import namedtuple
from typing import Tuple, List

import numpy as np
from matplotlib import pyplot as plt

Size = namedtuple('Size', 'width height')
Location = namedtuple('Location', 'x y')

PLOTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plots'))
SIMULATIONS_PATH = os.path.join(PLOTS_PATH, 'simulations')


def increment_filename(filepath: str):
    """ Increments the filepath by 1 until the new filepath does not exist.

    The expected format is '{filename}::{number}.{extension}'.
    """
    while os.path.exists(filepath):
        parts = filepath.split('.')
        prefix, extension = '.'.join(parts[:-1]), parts[-1]
        parts = prefix.split('::')
        filepath = f'{parts[0]}::{int(parts[1]) + 1}.{extension}'
    return filepath


def limits(min_x: int, max_x: int) -> Tuple[int, int]:
    """ Heuristic for assigning the lower and upper limits to population plots. """
    factor = 1000 if max_x > 2000 else 100 if max_x else 10 if max_x > 20 else 2
    return (min_x // factor - 1) * factor, min_x + factor * (1 + (max_x - min_x) // factor)


def _add_labels(ax, x, y, x_label, y_label, title, plotpath):
    # ax.set_xlim(limits(np.min(x), np.max(x)))
    # ax.set_ylim(limits(np.min(y), np.max(y)))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(plotpath, bbox_inches='tight', pad_inches=0.25)
    return


def line_plot(
        x: np.array,
        ys: List[np.array],
        colors: List[str],
        labels: List[str],
        x_label: str,
        y_label: str,
        title: str,
        plotpath: str,
):
    """ Plots continuous lines from the given data.

    :param x: x-values for all curves.
    :param ys: List of arrays, each stores the y-values for a single curve.
    :param colors: a List of color for each curve.
    :param labels: a List of labels for each curve.
    :param x_label: label for the x-axis.
    :param y_label: label for the y-axis.
    :param title: title for the plot.
    :param plotpath: filepath to save the plot.
    """
    if len(ys) != len(colors):
        raise ValueError(f'must have a color for each curve. '
                         f'Got {len(ys)} curves but {len(colors)} colors.')
    if len(ys) != len(labels):
        raise ValueError(f'must have a label for each curve. '
                         f'Got {len(ys)} curves but {len(labels)} labels.')
    if not all((len(y) == len(x) for y in ys)):
        print(x.shape, ys.shape)
        raise ValueError(f'All curves must have the same number of points as x-values. In this cane, {len(x)}.')

    fig = plt.figure(figsize=(16, 10), dpi=200)
    ax = fig.add_subplot(111)
    [plt.plot(x, ys[i], c=colors[i], label=labels[i], lw=1.) for i in range(len(colors))]
    _add_labels(ax, x, ys, x_label, y_label, title, plotpath)
    plt.close(fig)
    return


def arrow_plot(
        x: np.array,
        y: np.array,
        x_label: str,
        y_label: str,
        title: str,
        plotpath: str,
):
    """ Plots continuous lines from the given data.

    :param x: array of x-values.
    :param y: array of y-values.
    :param x_label: label for the x-axis.
    :param y_label: label for the y-axis.
    :param title: title for the plot.
    :param plotpath: filepath to save the plot.
    """
    if len(x.shape) != 1:
        raise ValueError(f'x must be a 1-d array. Got a {len(x.shape)}-d array instead')
    if x.shape != y.shape:
        raise ValueError(f'x and y must have the same shape. Got x {x.shape} and y {y.shape} instead.')

    fig = plt.figure(figsize=(16, 10), dpi=200)
    ax = fig.add_subplot(111)
    plt.quiver(x[:-1], y[:-1], x[1:] - x[:-1], y[1:] - y[:-1],
               scale_units='xy', angles='xy', scale=1, width=0.003)
    _add_labels(ax, x, y, x_label, y_label, title, plotpath)
    plt.close(fig)
    return
