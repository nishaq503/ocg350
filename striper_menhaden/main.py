import numpy as np
from board import Board
from utils import Size, Measurements

CANVAS_MULTIPLIER = 6


def simulate(time_steps: int) -> Measurements:
    if time_steps < 1:
        raise ValueError(f'must simulate for at least one time step. Got {time_steps}')

    bay = Board(size=Size(17, 11), predator_capacity=np.inf, prey_capacity=75)
    measurements: Measurements = list()

    measurements.append(bay.start(num_prey=3, num_predators=1))
    for _ in range(time_steps - 1):
        measurements.append(bay.step())

    return measurements


if __name__ == '__main__':
    print(np.asarray(simulate(20)))
