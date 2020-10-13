import os
from typing import List, Tuple, Union

from params import *
from simulate import draw_population_plot, draw_phase_plot, draw_difference_plots
from utils import EQUATIONS_PATH

# Redefining Populations for cleaner usage
Populations = List[Tuple[Union[int, float], Union[int, float]]]

# probability that a single pogy overlaps a single striper
PREY_PREDATOR_X = (PREY_SIZE.width + PREDATOR_SIZE.width) / BOARD_SIZE.width
PREY_PREDATOR_Y = (PREY_SIZE.height + PREDATOR_SIZE.height) / BOARD_SIZE.height
PREY_PREDATOR_OVERLAP = PREY_PREDATOR_X * PREY_PREDATOR_Y

# probability that two stripers are close enough to share a single pogy
PREDATOR_PREDATOR_OVERLAP = PREY_PREDATOR_OVERLAP * PREY_PREDATOR_OVERLAP

print(f'{PREY_PREDATOR_OVERLAP:e}, {PREDATOR_PREDATOR_OVERLAP:e}')


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


def simulate_once(time_steps: int, starting_pogies: int, starting_stripers: int, path: str):
    populations: Populations = [(starting_pogies, starting_stripers)]

    for _ in range(time_steps):
        prev_pogies, prev_stripers = populations[-1]
        next_pogies = next_num_pogies(prev_pogies, prev_stripers)
        next_stripers = next_num_stripers(prev_pogies, prev_stripers)
        populations.append((next_pogies, next_stripers))

    draw_population_plot(populations, os.path.join(path, 'population-vs-time.png'))
    draw_phase_plot(populations, os.path.join(path, 'phase-plot.png'))
    draw_difference_plots(
        populations,
        prey_plot_path=os.path.join(path, 'prey-difference.png'),
        predator_plot_path=os.path.join(path, 'predator-difference.png'),
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
        path=EQUATIONS_PATH
    )
