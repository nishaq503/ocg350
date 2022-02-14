import pathlib
import shutil
from typing import Optional

from PIL import Image

from board import Board
from params import *
from utils import *


def draw_population_plot(populations: np.array, filename: str):
    """ Draws a population vs time plot of the simulation.
    """
    time = np.arange(start=0, stop=populations.shape[1], dtype=int)

    line_plot(
        x=time,
        ys=populations,
        colors=['blue', 'red'],
        labels=['pogies', 'stripers'],
        x_label='time',
        y_label='population',
        title='populations vs time',
        plotpath=increment_filename(filename),
    )
    return


def draw_phase_plot(populations: np.array, filename: str):
    """ Draws a phase-plot of the population of the fish.
    """
    arrow_plot(
        x=populations[0, :],
        y=populations[1, :],
        x_label='pogies',
        y_label='stripers',
        title='striper population vs pogy population',
        plotpath=increment_filename(filename),
    )
    return


def draw_difference_plots(populations: np.array, prey_plot_path: str, predator_plot_path: str):
    """ Plots the population-difference vs population plots for both species. """
    prey_population = populations[0, :][:-1]
    prey_delta = populations[0, :][1:] - prey_population
    arrow_plot(
        x=prey_population,
        y=prey_delta,
        x_label='population',
        y_label='delta',
        title='pogies difference vs population',
        plotpath=increment_filename(prey_plot_path),
    )

    predator_population = populations[1, :][:-1]
    predator_delta = populations[1, :][1:] - predator_population
    arrow_plot(
        x=predator_population,
        y=predator_delta,
        x_label='population',
        y_label='delta',
        title='stripers difference vs population',
        plotpath=increment_filename(predator_plot_path),
    )
    return


def simulate_once(size_multiplier: int, time_steps: int, gif_path: Optional[str] = None) -> np.array:
    """
    Runs a single simulation of the model.

    :param size_multiplier: size multiplier of board anc capacity.
    :param time_steps: Number of time steps for which to run the model.
    :param gif_path: file path where the animation may be saved.
    """
    if time_steps < 1:
        raise ValueError(f'must simulate for at least one time step. Got {time_steps}')

    bay = Board(
        size=Size(BOARD_SIZE.width * size_multiplier, BOARD_SIZE.height * size_multiplier),
        prey_capacity=PREY_CAPACITY * (size_multiplier ** 2),
    )
    populations: np.array = np.zeros(shape=(2, time_steps))
    images: List[Image] = list()

    for i in range(time_steps):
        end = ',\n' if (i + 1) % 20 == 0 else ', '
        print(f'{i + 1}', end=end)
        populations[:, i] = bay.step()
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
            duration=1_000 if size_multiplier > 1 else 1_500,  # each frame is shown for this many milliseconds.
        )
    return populations


def main(
        size_multiplier: int,
        erase: bool = False,
        animate: bool = ANIMATE,
        num_simulations: int = NUM_SIMULATIONS,
        time_steps: int = TIME_STEPS,
):
    if (not isinstance(size_multiplier, int)) or (size_multiplier < 1):
        raise ValueError(f'The Size Multiplier must be an integer, and be at least 1.')

    # Remove old files if necessary
    plots_dir = os.path.join(SIMULATIONS_PATH, f'multiplier_{size_multiplier}')
    if erase:
        shutil.rmtree(plots_dir)
    plots_dir = os.path.join(SIMULATIONS_PATH, f'multiplier_{size_multiplier}', f'sim__0__')
    pathlib.Path(plots_dir).mkdir(exist_ok=True, parents=True)

    # create file names for the first of each plot
    population_path = os.path.join(plots_dir, '1-populations-vs-time.png')
    phase_path = os.path.join(plots_dir, '2-phase-plot.png')
    prey_difference_path = os.path.join(plots_dir, '3-prey-difference.png')
    predator_difference_path = os.path.join(plots_dir, '4-predator-difference.png')
    gif_path = os.path.join(plots_dir, '5-animation.gif')

    # run simulation for the requested number of times.
    np.random.seed(0)
    for i in range(num_simulations):
        print(f'Starting simulation number {i + 1}, with size multiplier {size_multiplier}.')
        if (i == 0) and animate:
            populations = simulate_once(size_multiplier=size_multiplier, time_steps=time_steps, gif_path=gif_path)
        else:
            populations = simulate_once(size_multiplier=size_multiplier, time_steps=time_steps, gif_path=None)
        draw_population_plot(populations, population_path)
        draw_phase_plot(populations, phase_path)
        draw_difference_plots(populations, prey_difference_path, predator_difference_path)
    return


if __name__ == '__main__':
    main(size_multiplier=1)
    # main(size_multiplier=5)
