from abc import ABC, abstractmethod
from typing import Callable, Set

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
    def __init__(self, size: Size):
        self.size: Size = size
        self.location: Location = None
        self.children: int = 0

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
    def reproduce(self, function: Callable[[float], int]) -> 'Fish':
        pass


class Prey(Fish):
    """
    Fish that gets eaten in a predator-prey model.

    This class defines those properties and methods that are specific to prey fish.
    """
    def __init__(
            self,
            size: Size = PREY_SIZE,
            reproduction_rate: float = PREY_REPRODUCTION_RATE,
    ):
        """
        Creates an object representing a Prey Fish.

        :param size: the size of the fish.
        :param reproduction_rate: Reproduction rate (between 0 and 1) of the fish.
        """
        super().__init__(size)
        if 0 <= reproduction_rate <= 1:
            self.reproduction_rate: float = reproduction_rate
        else:
            raise ValueError(f'Reproduction rate must be in the [0, 1] range. Got {reproduction_rate:.2f} instead.')
        self.got_eaten: bool = False

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
    def __init__(self, size: Size = PREDATOR_SIZE):
        super().__init__(size)
        self.num_eaten: int = 0

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
