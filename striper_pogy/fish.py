from abc import ABC, abstractmethod
from typing import Callable, Set, Tuple

import numpy as np
from PIL import ImageDraw

from utils import (
    Size,
    Location,
    PREDATOR_SIZE,
    PREY_SIZE,
    PREY_REPRODUCTION_RATE,
    prey_reproduction_function,
    predator_reproduction_function,
)


class Fish(ABC):
    """
    An abstract Fish class.

    This defines properties and methods that are common to all fish.
    """
    def __init__(self, board_size: Size, fish_size: Size):
        self.size: Size = fish_size
        self.location: Location = self._drop(board_size)
        self.children: int = 0

        # outline and fill are for drawing the fish as rectangles
        self.outline: Tuple[int, int, int] = (0, 0, 0)
        self.fill: Tuple[int, int, int] = tuple()

    @property
    def width(self) -> float:
        return self.size.width

    @property
    def height(self) -> float:
        return self.size.height

    @property
    def x(self) -> float:
        return self.location.x

    @property
    def y(self) -> float:
        return self.location.y

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def reproduce(self, function: Callable[[float], int]) -> 'Fish':
        pass

    def _drop(self, board_size: Size) -> Location:
        """
        Drop the fish onto the board and assign location.

        :param board_size: of the board on which to drop.
        :return: nothing.
        """
        def sample(margin: float, length: float) -> float:
            """ Uniform random sample over length, excluding margin from each end. """
            return np.random.uniform(low=margin, high=length - margin)

        x: float = sample(self.width / 2, board_size.width)
        y: float = sample(self.height / 2, board_size.height)
        return Location(x, y)

    def draw(self, draw: ImageDraw, scale: float) -> None:
        half_width, half_height = self.width / 2, self.height / 2
        x1, y1 = self.x - half_width, self.y - half_height
        x2, y2 = self.x + half_width, self.y + half_height
        xy = x1 * scale, y1 * scale, x2 * scale, y2 * scale
        draw.rectangle(xy, fill=self.fill, outline=self.outline)
        return


class Prey(Fish):
    """
    Fish that gets eaten in a predator-prey model.

    This class defines those properties and methods that are specific to prey fish.
    """
    def __init__(
            self,
            board_size: Size,
            fish_size: Size = PREY_SIZE,
            reproduction_rate: float = PREY_REPRODUCTION_RATE,
    ):
        """
        Creates an object representing a Prey Fish.

        :param board_size: the size of the board on which to simulate the predator-prey model.
        :param fish_size: the size of the fish.
        :param reproduction_rate: Reproduction rate (between 0 and 1) of the fish.
        """
        super().__init__(board_size, fish_size)
        if 0 <= reproduction_rate <= 1:
            self.reproduction_rate: float = reproduction_rate
        else:
            raise ValueError(f'Reproduction rate must be in the [0, 1] range. Got {reproduction_rate:.2f} instead.')
        self.fill: Tuple[int, int, int] = (0, 0, 255)  # blue

        self.got_eaten: bool = False

    def __hash__(self):
        return hash(f'prey ({self.x:.2f},{self.y:.2f})')

    def reproduce(self, function: Callable[[float], int] = prey_reproduction_function) -> 'Prey':
        """
        The fish has either one or two children based on its reproduction rate.

        :param function: reproduction function to use.
        :return: the fish modified with its number of children.
        """
        self.children = 0 if self.got_eaten else function(self.reproduction_rate)
        return self


class Predator(Fish):
    """
    Fish that eats in a predator-prey model.

    This class defines those properties and methods tha are specific to predator fish.
    """
    def __init__(self, board_size: Size, fish_size: Size = PREDATOR_SIZE):
        super().__init__(board_size, fish_size)
        self.fill: Tuple[int, int, int] = (255, 0, 0)  # red

        self.num_eaten: int = 0

    def __hash__(self):
        return hash(f'predator ({self.x:.2f},{self.y:.2f})')

    def touches(self, prey: Prey) -> bool:
        """
        Checks to see if the predator touches the prey.

        :param prey: prey to check against.
        :return: whether the predator touches the prey.
        """
        x_delta: float = abs(self.x - prey.x)
        x_margin: float = (self.width + prey.width) / 2

        y_delta: float = abs(self.y - prey.y)
        y_margin: float = (self.height + prey.height) / 2

        return x_delta <= x_margin and y_delta <= y_margin

    def eat(self, food: Set[Prey]) -> 'Predator':
        """
        Have the Predator eat the given number of Prey.

        :param food: fish to be eaten
        :return: the predator modified with the number of fish eaten.
        """
        for fish in food:
            fish.got_eaten = True
        self.num_eaten = len(food)
        return self

    def reproduce(self, function: Callable[[int], int] = predator_reproduction_function) -> 'Predator':
        """
        Let the Predator reproduce based on the number of fish it ate.

        :param function: reproduction function to use.
        :return: the predator modified by the number of children its going to have.
        """
        self.children = function(self.num_eaten)
        return self
