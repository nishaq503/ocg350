import os
from typing import List, Tuple, Union

from params import *
from simulate import draw_population_plot, draw_phase_plot, draw_difference_plots
from utils import EQUATIONS_PATH

# Redefining Populations for cleaner usage
Populations = List[Tuple[Union[int, float], Union[int, float]]]

PREY_MARGIN = (BOARD_SIZE.width - PREY_SIZE.width) * (BOARD_SIZE.height - PREY_SIZE.height)
PREDATOR_MARGIN = (BOARD_SIZE.width - PREDATOR_SIZE.width) * (BOARD_SIZE.height - PREDATOR_SIZE.height)

PREDATOR_PREY_AREA = (PREDATOR_SIZE.width + PREY_SIZE.width) * (PREDATOR_SIZE.height + PREY_SIZE.height)
PREY_PREDATOR_OVERLAP = PREDATOR_PREY_AREA / PREY_MARGIN

PREDATOR_PREDATOR_AREA = (PREDATOR_SIZE.width * 2) * (PREDATOR_SIZE.height * 2)
PREDATOR_PREDATOR_OVERLAP = PREDATOR_PREDATOR_AREA / PREDATOR_MARGIN


def next_num_pogies(num_pogies: float, num_stripers: float) -> float:
    # pogy population above which reproduction rate falls
    if num_pogies < PREY_CAPACITY / (1 + PREY_REPRODUCTION_RATE):
        reproduction_rate = PREY_REPRODUCTION_RATE
    else:
        reproduction_rate = PREY_CAPACITY / num_pogies - 1
    survival_rate = (1 - PREY_PREDATOR_OVERLAP) ** num_stripers
    next_num = (1 + reproduction_rate) * num_pogies * survival_rate
    return max(min(next_num, PREY_CAPACITY), 3)


def next_num_stripers(num_pogies: float, num_stripers: float) -> float:
    num_eaten = num_pogies * (1 - (1 - PREY_PREDATOR_OVERLAP) ** num_stripers)
    self_competition = ((1 - PREDATOR_PREDATOR_OVERLAP) ** num_stripers)
    next_num = (num_eaten / PREDATOR_FOOD_REQUIREMENTS) * self_competition
    return max(next_num, 1)


# noinspection DuplicatedCode
def simulate_once(time_steps: int, starting_pogies: int, starting_stripers: int, plots_path: str):
    populations: Populations = [(starting_pogies, starting_stripers)]

    for _ in range(time_steps):
        prev_pogies, prev_stripers = populations[-1]
        next_pogies = next_num_pogies(prev_pogies, prev_stripers)
        next_stripers = next_num_stripers(prev_pogies, prev_stripers)
        populations.append((next_pogies, next_stripers))

    os.makedirs(plots_path, exist_ok=True)
    if ERASE:
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
    population_path = os.path.join(population_dir, 'plot::0.png')
    phase_path = os.path.join(phase_dir, 'plot::0.png')
    prey_difference_path = os.path.join(prey_difference_dir, 'plot::0.png')
    predator_difference_path = os.path.join(predator_difference_dir, 'plot::0.png')

    draw_population_plot(populations, population_path)
    draw_phase_plot(populations, phase_path)
    draw_difference_plots(
        populations,
        prey_plot_path=prey_difference_path,
        predator_plot_path=predator_difference_path,
    )

    return


if __name__ == '__main__':
    os.makedirs(EQUATIONS_PATH, exist_ok=True)
    if ERASE:
        for _root, _, _files in os.walk(EQUATIONS_PATH):
            [os.remove(os.path.join(_root, _file)) for _file in _files]

    simulate_once(
        time_steps=TIME_STEPS,
        starting_pogies=STARTING_PREY,
        starting_stripers=STARTING_PREDATORS,
        plots_path=EQUATIONS_PATH
    )
