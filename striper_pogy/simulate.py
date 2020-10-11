import os
from typing import Optional, List

import numpy as np
from PIL import Image

from board import Board
from params import *
from utils import Populations, increment_filename, GAME_PATH, line_plot, arrow_plot


def simulate_once(time_steps: int, gif_path: Optional[str] = None) -> Populations:
    """
    Runs a single simulation of the model.

    :param time_steps: Number of time steps for which to run the model.
    :param gif_path: file path where the animation may be saved.
    """
    if time_steps < 1:
        raise ValueError(f'must simulate for at least one time step. Got {time_steps}')

    bay = Board()
    populations: Populations = list()
    images: List[Image] = list()

    # _ in Python is a throwaway variable.
    for _ in range(time_steps):
        populations.append(bay.step())
        if gif_path is not None:
            im = bay.draw()
            images.append(im)

    # only create the animation if a path is provided.
    if gif_path is not None:
        gif_path = increment_filename(gif_path)
        images[0].save(
            gif_path,
            save_all=True,  # save all images in gif.
            optimize=True,  # reduces final filesize of the gif.
            append_images=images[1:],  # ordered list of other images.
            duration=1_250,  # each frame is shown for these many milliseconds.
        )
        pass

    return populations


def draw_population_plot(populations: Populations, filename: str):
    """ Draws a population vs time plot of the simulation.
    """
    time = np.arange(start=0, stop=len(populations), dtype=int)
    pogies = np.asarray([m[0] for m in populations], dtype=int)
    stripers = np.asarray([m[1] for m in populations], dtype=int)

    line_plot(
        x=time,
        ys=[pogies, stripers],
        curve_colors=['blue', 'red'],
        curve_labels=['pogies', 'stripers'],
        plot_size=(16, 10),
        dpi=200,
        x_label='time',
        y_label='population',
        title='populations vs time',
        filename=increment_filename(filename),
    )
    return


def draw_phase_plot(populations: Populations, filename: str):
    """ Draws a phase-plot of the population of the fish.
    """
    arrow_plot(
        x=np.asarray([m[0] for m in populations], dtype=int),
        y=np.asarray([m[1] for m in populations], dtype=int),
        plot_size=(16, 10),
        dpi=200,
        x_label='pogies',
        y_label='stripers',
        title='striper population vs pogy population',
        filename=increment_filename(filename),
    )
    return


def draw_difference_plots(populations: Populations, prey_plot_path: str, predator_plot_path: str):
    """ Plots the population-difference vs population plots for both species. """
    prey_population = np.asarray([m[0] for m in populations], dtype=int)[:-1]
    prey_delta = np.asarray([m[0] for m in populations], dtype=int)[1:] - prey_population
    arrow_plot(
        x=prey_population,
        y=prey_delta,
        plot_size=(16, 10),
        dpi=200,
        x_label='population',
        y_label='delta',
        title='pogies difference vs population',
        filename=increment_filename(prey_plot_path),
    )

    predator_population = np.asarray([m[1] for m in populations], dtype=int)[:-1]
    predator_delta = np.asarray([m[1] for m in populations], dtype=int)[1:] - predator_population
    arrow_plot(
        x=predator_population,
        y=predator_delta,
        plot_size=(16, 10),
        dpi=200,
        x_label='population',
        y_label='delta',
        title='stripers difference vs population',
        filename=increment_filename(predator_plot_path),
    )
    return


if __name__ == '__main__':
    # Create required directories and remove old files if necessary
    os.makedirs(GAME_PATH, exist_ok=True)
    if ERASE:
        for _root, _, _files in os.walk(GAME_PATH):
            [os.remove(os.path.join(_root, _file)) for _file in _files]

    _population_dir = os.path.join(GAME_PATH, 'population-vs-time')
    _phase_dir = os.path.join(GAME_PATH, 'phase-plots')
    _prey_difference_dir = os.path.join(GAME_PATH, 'prey-difference')
    _predator_difference_dir = os.path.join(GAME_PATH, 'predator-difference')

    [os.makedirs(_dir, exist_ok=True) for _dir in [
        _population_dir,
        _phase_dir,
        _prey_difference_dir,
        _predator_difference_dir
    ]]

    # create file names for the first of each plot
    _gif_path = os.path.join(GAME_PATH, 'animation.gif')
    _population_path = os.path.join(_population_dir, 'plot::0.png')
    _phase_path = os.path.join(_phase_dir, 'plot::0.png')
    _prey_difference_path = os.path.join(_prey_difference_dir, 'plot::0.png')
    _predator_difference_path = os.path.join(_predator_difference_dir, 'plot::0.png')

    # run simulation for the requested number of times.
    np.random.seed(0)
    for _i in range(NUM_SIMULATIONS):
        if (_i == 0) and ANIMATE:
            _populations = simulate_once(time_steps=TIME_STEPS, gif_path=_gif_path)
        else:
            _populations = simulate_once(time_steps=TIME_STEPS, gif_path=None)
        draw_population_plot(_populations, _population_path)
        draw_phase_plot(_populations, _phase_path)
        draw_difference_plots(_populations, _prey_difference_path, _predator_difference_path)
