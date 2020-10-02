import os
from typing import List, Tuple

import numpy as np
from collections import namedtuple

PLOTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plots'))

Size = namedtuple('Size', 'width height')
Location = namedtuple('Location', 'x y')
Measurements = List[Tuple[int, int]]


def increment_filename(filename: str):
    while os.path.exists(filename):
        prefix = filename[:-4]  # remove file extension
        parts = prefix.split('::')
        number = int(parts[-1]) + 1  # increment plot number
        filename = f'{parts[0]}::{number}.png'
    return filename


# Parameters that can be tweaked

BOARD_SIZE: Size = Size(17, 11)

PREY_SIZE: Size = Size(1, 1)
PREY_CAPACITY: int = 75
PREY_REPRODUCTION_RATE: float = 0.5

PREDATOR_SIZE: Size = Size(2.5, 2.5)
PREDATOR_CAPACITY: int = np.inf
PREDATOR_FOOD_REQUIREMENTS: int = 3


def predator_reproduction_function(num_eaten: int) -> int:
    return num_eaten // PREDATOR_FOOD_REQUIREMENTS


def prey_reproduction_function(reproduction_rate: float) -> int:
    return 2 if np.random.uniform() < reproduction_rate else 1
