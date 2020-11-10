from abc import ABC, abstractmethod
from typing import Set

from PIL import ImageDraw

from params import *
from utils import *


class Fish(ABC):
    """ This class represents an abstract fish.

    This class defines properties that are common to all fish.
    """
    def __init__(self, board_size: Size, fish_size: Size):
        """ Creates a fish and drops it on the board. """
        if any((f <= 0 for f in fish_size)):
            raise ValueError(f'The width and height of the fish must be positive numbers. Got {fish_size} instead.')
        self.size: Size = fish_size

        if any((f <= 0 for f in board_size)):
            raise ValueError(f'The width and height of the board must be positive numbers. Got {board_size} instead.')
        self.location: Location = self._drop(board_size)

        self.children: int = 0
        self.outline: Tuple[int, int, int] = 0, 0, 0
        self.fill: Tuple[int, int, int] = tuple()

    def __str__(self) -> str:
        return f'({self.x:.2f},{self.y:.2f})'

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
    def reproduce(self, *args) -> 'Fish':
        pass

    def _drop(self, board_size: Size) -> Location:
        def sample(margin: float, length: float) -> float:
            """ Uniform random sample from the board. """
            return np.random.uniform(low=margin, high=length - margin)

        x: float = sample(self.width / 2, board_size.width)
        y: float = sample(self.height / 2, board_size.height)
        return Location(x, y)

    def draw(self, draw: ImageDraw, scale: float):
        half_width, half_height = self.width / 2, self.height / 2
        x1, y1 = self.x - half_width, self.y - half_height
        x2, y2 = self.x + half_width, self.y + half_height
        xy = x1 * scale, y1 * scale, x2 * scale, y2 * scale
        fill = self.fill if self.children > 0 else (211, 211, 211)
        draw.rectangle(xy, fill=fill, outline=self.outline)
        return


class Prey(Fish):
    """ A class to represent the Prey fish.

    This class defines properties and methods that are specific to prey.
    """
    def __init__(self, board_size: Size, fish_size: Size = PREY_SIZE):
        """ Creates a Prey fish, drops it on the board, and defines its color. """
        super().__init__(board_size, fish_size)
        self.fill = (0, 0, 255)  # blue
        self.got_eaten = False

    def __hash__(self) -> int:
        return hash(f'prey {str(self)}')

    def reproduce(self, rate: float = PREY_REPRODUCTION_RATE) -> 'Fish':
        """ A prey can have one or two children, depending on reproduction rate, if it was not eaten.

        :param rate: The reproduction rate to use.
        :return: the modified prey with its number of children.
        """
        if rate < 0:
            raise ValueError(f'Prey reproduction rate must be a non-negative number. Got {rate:.3f} instead.')

        self.children = 0 if self.got_eaten else 1 if np.random.uniform() > rate else 2
        return self


class Predator(Fish):
    """ A class to represent the Predator fish.

    This class defines properties and methods that are specific to predators.
    """
    def __init__(self, board_size: Size, fish_size: Size = PREDATOR_SIZE):
        """ Creates a Predator fish, drops it on the board, amd defines its color. """
        super().__init__(board_size, fish_size)
        self.fill = (255, 0, 0)  # red
        self.num_eaten: int = 0

    def __hash__(self) -> int:
        return hash(f'predator {str(self)}')

    def touches(self, prey: Prey) -> bool:
        """ Checks to see if this predator touches the given prey.

        :param prey: prey to check against.
        :return: whether the predator touches the prey.
        """
        x_delta: float = abs(self.x - prey.x)
        x_margin: float = (self.width + prey.width) / 2

        y_delta: float = abs(self.y - prey.y)
        y_margin: float = (self.height + prey.height) / 2

        return x_delta <= x_margin and y_delta <= y_margin

    def eat(self, food: Set[Prey]) -> 'Predator':
        """ Have this Predator eat the given set of Prey.

        :param food: a set of fish to be eaten.
        :return: the modified predator with the number of fish eaten.
        """
        for fish in food:
            fish.got_eaten = True
        self.num_eaten = len(food)
        return self

    def reproduce(self, food_requirement: float = PREDATOR_FOOD_REQUIREMENTS) -> 'Predator':
        """ Let this Predator reproduce based on the number of fish it ate.

        :param food_requirement: the food requirement threshold for reproduction.
        :return: the modified predator with the number of children its going to have.
        """
        if food_requirement < 0:
            raise ValueError(f'Predator food requirements must be positive. Got {food_requirement:.3f} instead.')
        self.children = int(np.floor(self.num_eaten / food_requirement))
        return self
