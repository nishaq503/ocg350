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
        plot_size=(7, 3),
        dpi=100,
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
        plot_size=(7, 3),
        dpi=100,
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
        plot_size=(7, 3),
        dpi=100,
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
        plot_size=(7, 3),
        dpi=100,
        x_label='population',
        y_label='delta',
        title='stripers difference vs population',
        filename=increment_filename(predator_plot_path),
    )
    return


def main(
        plots_path: str = GAME_PATH,
        erase: bool = ERASE,
        animate: bool = ANIMATE,
        num_simulations: int = NUM_SIMULATIONS,
        time_steps: int = TIME_STEPS,
):
    # Create required directories and remove old files if necessary
    os.makedirs(plots_path, exist_ok=True)
    if erase:
        for root, _, files in os.walk(plots_path):
            [os.remove(os.path.join(root, file)) for file in files]

    population_dir = os.path.join(plots_path, 'population-vs-time')
    phase_dir = os.path.join(plots_path, 'phase-plots')
    prey_difference_dir = os.path.join(plots_path, 'prey-difference')
    predator_difference_dir = os.path.join(plots_path, 'predator-difference')

    [os.makedirs(_dir, exist_ok=True) for _dir in [
        population_dir,
        phase_dir,
        prey_difference_dir,
        predator_difference_dir
    ]]

    # create file names for the first of each plot
    gif_path = os.path.join(plots_path, 'animation.gif')
    population_path = os.path.join(population_dir, 'plot::0.png')
    phase_path = os.path.join(phase_dir, 'plot::0.png')
    prey_difference_path = os.path.join(prey_difference_dir, 'plot::0.png')
    predator_difference_path = os.path.join(predator_difference_dir, 'plot::0.png')

    # run simulation for the requested number of times.
    np.random.seed(0)
    for i in range(num_simulations):
        if (i == 0) and animate:
            populations = simulate_once(time_steps=time_steps, gif_path=gif_path)
        else:
            populations = simulate_once(time_steps=time_steps, gif_path=None)
        draw_population_plot(populations, population_path)
        draw_phase_plot(populations, phase_path)
        draw_difference_plots(populations, prey_difference_path, predator_difference_path)

    return


if __name__ == '__main__':
    main()
