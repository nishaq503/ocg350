import os
from typing import Optional, List, Dict

import numpy as np
from PIL import Image

from board import Board
from utils import Populations, increment_filename, GAME_PATH, line_plot, arrow_plot


def simulate_once(time_steps: int, gif_path: Optional[str] = None) -> Populations:
    if time_steps < 1:
        raise ValueError(f'must simulate for at least one time step. Got {time_steps}')

    bay = Board()
    populations: Populations = list()
    images: List[Image] = list()

    for _ in range(time_steps):
        populations.append(bay.step())
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

    return populations


def draw_population_plot(populations: Populations, filename: str):
    x = np.arange(start=0, stop=len(populations), dtype=int)
    y1 = np.asarray([m[0] for m in populations], dtype=int)
    y2 = np.asarray([m[1] for m in populations], dtype=int)

    line_plot(
        x=x,
        ys=[y1, y2],
        curve_colors=['blue', 'red'],
        curve_labels=['pogies', 'stripers'],
        plot_size=(7, 3),
        dpi=100,
        x_label='time',
        y_label='population',
        title='populations of stripers and menhaden against time',
        filename=increment_filename(filename),
    )
    return


def draw_phase_plot(populations: Populations, filename: str):
    arrow_plot(
        x=np.asarray([m[0] for m in populations], dtype=int),
        y=np.asarray([m[1] for m in populations], dtype=int),
        plot_size=(7, 3),
        dpi=100,
        x_label='pogies',
        y_label='stripers',
        title='phase plot of striper population vs pogy population',
        filename=increment_filename(filename),
    )
    return


def draw_difference_plots(populations: Populations, prey_plot_path: str, predator_plot_path: str):
    prey_population = np.asarray([m[0] for m in populations], dtype=int)[:-1]
    prey_delta = np.asarray([m[0] for m in populations], dtype=int)[1:] - prey_population
    arrow_plot(
        x=prey_population,
        y=prey_delta,
        plot_size=(7, 3),
        dpi=100,
        x_label='population',
        y_label='delta',
        title='pogies delta vs population',
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
        title='stripers delta vs population',
        filename=increment_filename(predator_plot_path),
    )
    return


def create_paths(directory: str, erase: bool) -> Dict[str, str]:
    os.makedirs(directory, exist_ok=True)
    if erase:
        for root, _, files in os.walk(directory):
            [os.remove(os.path.join(root, file)) for file in files]

    gif_dir = os.path.join(directory, 'simulations')
    population_dir = os.path.join(directory, 'population-vs-time')
    phase_dir = os.path.join(directory, 'phase-plots')
    prey_difference_dir = os.path.join(directory, 'pogies-delta')
    predator_difference_dir = os.path.join(directory, 'stripers-delta')

    [os.makedirs(_dir, exist_ok=True) for _dir in [
        gif_dir,
        population_dir,
        phase_dir,
        prey_difference_dir,
        predator_difference_dir
    ]]

    return {
        'gif_path': os.path.join(gif_dir, 'simulation::0.gif'),
        'population_path': os.path.join(population_dir, 'plot::0.png'),
        'phase_path': os.path.join(phase_dir, 'plot::0.png'),
        'prey_difference_path': os.path.join(prey_difference_dir, 'plot::0.png'),
        'predator_difference_path': os.path.join(predator_difference_dir, 'plot::0.png'),
    }


def simulate_multiple(directory: str, time_steps: int, num_simulations: int, animate: bool):
    paths: Dict[str, str] = create_paths(directory, erase=False)
    for i in range(num_simulations):
        if (i == 0) and animate:
            populations = simulate_once(time_steps=time_steps, gif_path=paths['gif_path'])
        else:
            populations = simulate_once(time_steps=time_steps, gif_path=None)
        draw_population_plot(populations, paths['population_path'])
        draw_phase_plot(populations, paths['phase_path'])
        draw_difference_plots(populations, paths['prey_difference_path'], paths['predator_difference_path'])
    return


if __name__ == '__main__':
    np.random.seed(0)
    simulate_multiple(GAME_PATH, time_steps=128, num_simulations=1, animate=False)
