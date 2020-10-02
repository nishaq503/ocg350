from typing import List, Tuple

import numpy as np
from collections import namedtuple

Size = namedtuple('Size', 'width height')
Location = namedtuple('Location', 'x y')
Measurements = List[Tuple[int, int]]

PREDATOR_SIZE: Size = Size(2.5, 2.5)
PREY_SIZE: Size = Size(1, 1)
PREY_REPRODUCTION_RATE: float = 0.5
PREDATOR_FOOD_REQUIREMENTS: int = 3


def predator_reproduction_function(num_eaten: int) -> int:
    return num_eaten // PREDATOR_FOOD_REQUIREMENTS


def prey_reproduction_function(reproduction_rate: float) -> int:
    return 2 if np.random.uniform() < reproduction_rate else 1
