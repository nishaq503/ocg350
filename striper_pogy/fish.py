from abc import ABC, abstractmethod
from typing import Set, Tuple

import numpy as np
from PIL import ImageDraw

from params import PREY_SIZE, PREY_REPRODUCTION_RATE, PREDATOR_SIZE, PREDATOR_FOOD_REQUIREMENTS
from utils import Size, Location


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
    def reproduce(self, *args) -> 'Fish':
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
        fill = self.fill if self.children > 0 else (211, 211, 211)
        draw.rectangle(xy, fill=fill, outline=self.outline)
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
    ):
        """
        Creates an object representing a Prey Fish.

        :param board_size: the size of the board on which to simulate the predator-prey model.
        :param fish_size: the size of the fish.
        """
        super().__init__(board_size, fish_size)
        self.fill: Tuple[int, int, int] = (0, 0, 255)  # blue
        self.got_eaten: bool = False

    def __hash__(self):
        return hash(f'prey ({self.x:.2f},{self.y:.2f})')

    def reproduce(self, rate: float = PREY_REPRODUCTION_RATE) -> 'Prey':
        """
        The fish has either one or two children based on its reproduction rate.

        :param rate: enter reproduction rate to use instead of default rate.
        :return: the fish modified with its number of children.
        """
        self.children = 0 if self.got_eaten else 1 if np.random.uniform() < rate else 2
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

    def reproduce(self, food_requirement: float = PREDATOR_FOOD_REQUIREMENTS) -> 'Predator':
        """
        Let the Predator reproduce based on the number of fish it ate.

        :param food_requirement: enter food requirement to use instead of default value
        :return: the predator modified by the number of children its going to have.
        """
        self.children = int(np.floor(self.num_eaten / food_requirement))
        return self
