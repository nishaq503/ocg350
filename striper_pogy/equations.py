from typing import Dict

from simulate import draw_population_plot, draw_phase_plot, draw_difference_plots, create_paths
from utils import PREY_REPRODUCTION_RATE as R_M, PREY_CAPACITY as K, PREY_SIZE, PREDATOR_SIZE, BOARD_SIZE, Populations, EQUATIONS_PATH

# pogy population above which reproduction rate falls
R_MARGIN = K / (1 + R_M)

# probability that prey and predator overlap
PREY_PREDATOR_X = (PREY_SIZE.width + PREDATOR_SIZE.width) / BOARD_SIZE.width
PREY_PREDATOR_Y = (PREY_SIZE.height + PREDATOR_SIZE.height) / BOARD_SIZE.height
PREY_PREDATOR_OVERLAP = PREY_PREDATOR_X * PREY_PREDATOR_Y

# probability that two predators are close enough to share fish
PREDATOR_PREDATOR_OVERLAP = PREY_PREDATOR_OVERLAP * PREY_PREDATOR_OVERLAP


def next_num_pogies(num_pogies: float, num_stripers: float) -> float:
    reproduction_rate = R_M if num_pogies < R_MARGIN else K / num_pogies - 1
    survival_rate = (1 - PREY_PREDATOR_OVERLAP) ** num_stripers
    next_num = (1 + reproduction_rate) * num_pogies * survival_rate
    return max(next_num, 3.)


def next_num_stripers(num_pogies: float, num_stripers: float) -> float:
    num_eaten = num_pogies * (1 - (1 - PREY_PREDATOR_OVERLAP) ** num_stripers)
    self_competition = ((1 - PREDATOR_PREDATOR_OVERLAP) ** num_stripers)
    next_num = (num_eaten / 3) * self_competition
    return max(next_num, 1)


def simulate_once(time_steps: int, starting_pogies: int, starting_stripers: int, paths: Dict[str, str]):
    populations: Populations = [(starting_pogies, starting_stripers)]

    for _ in range(time_steps):
        prev_pogies, prev_stripers = populations[-1]
        next_pogies = next_num_pogies(prev_pogies, prev_stripers)
        next_stripers = next_num_stripers(prev_pogies, prev_stripers)
        populations.append((next_pogies, next_stripers))

    draw_population_plot(populations, paths['population_path'])
    draw_phase_plot(populations, paths['phase_path'])
    draw_difference_plots(populations, paths['prey_difference_path'], paths['predator_difference_path'])

    return


if __name__ == '__main__':
    simulate_once(128, 3, 1, create_paths(EQUATIONS_PATH, erase=True))
