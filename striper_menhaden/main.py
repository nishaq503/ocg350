import numpy as np
from board import Board
import utils
from utils import Size, Measurements

CANVAS_MULTIPLIER = 6


def simulate(
        time_steps: int,
        board_size: Size = None,
        prey_capacity: int = None,
        predator_capacity: int = None,
) -> Measurements:
    if time_steps < 1:
        raise ValueError(f'must simulate for at least one time step. Got {time_steps}')

    if board_size is None:
        board_size = Size(17, 11)
    if prey_capacity is None:
        prey_capacity = np.inf
    if predator_capacity is None:
        predator_capacity = np.inf

    bay = Board(
        board_size,
        prey_capacity=prey_capacity,
        predator_capacity=predator_capacity,
    )
    measurements: Measurements = list()

    measurements.append(bay.start(num_prey=3, num_predators=1))
    for _ in range(time_steps - 1):
        measurements.append(bay.step())

    return measurements


if __name__ == '__main__':
    np.random.seed(42)
    utils.PREDATOR_SIZE = Size(2.5, 2.5)
    utils.PREY_SIZE = Size(1, 1)
    utils.PREY_REPRODUCTION_RATE = 1
    utils.PREDATOR_FOOD_REQUIREMENTS = 3

    _measurements = simulate(
        time_steps=50,
        board_size=Size(17, 11),
        prey_capacity=75,
    )
    print(np.asarray(_measurements))
