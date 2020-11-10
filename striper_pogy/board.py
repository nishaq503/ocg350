import numpy as np
from typing import Set, Tuple, Optional

from PIL import Image, ImageDraw, ImageFont

from fish import Predator, Prey
from params import *
from utils import Size


class Board:
    def __init__(
            self,
            size: Size,
            prey_capacity: int,
            *,  # any arguments after '*' must be passed by name.
            starting_prey: int = STARTING_PREY,
            starting_predators: int = STARTING_PREDATORS,
            fishery: Optional[float] = FISHERY
    ):
        """ Initializes a board with a given size.

        :param size: The (width, height) of board to use.
        :param prey_capacity: carrying capacity of the prey.
        :param starting_prey: number of prey with which to start a simulation.
        :param starting_predators: number of predators with which to start a simulation.
        :param fishery: fraction of prey to remove each time step dur to fishing.
        """
        if any((s <= 0 for s in size)):
            raise ValueError(f'The dimensions of the board must be positive numbers. Got ({size} instead')
        self.size: Size = size

        if not (starting_prey > 0):
            raise ValueError(f'Must start with at least one prey fish. Got {starting_prey} instead')
        self.starting_prey = starting_prey

        if not (prey_capacity > 0):
            raise ValueError(f'Prey capacity must be a positive number. Got {prey_capacity} instead')
        self.prey_capacity: int = prey_capacity

        if not (starting_predators > 0):
            raise ValueError(f'Must start with at least one predator fish. Got {starting_predators} instead')
        self.starting_predators = starting_predators

        if fishery is not None:
            if not (0 <= fishery <= 1):
                raise ValueError(f'fishery fraction must be between 0 and 1. Got {fishery:.2f} instead.')
        self.fishery: Optional[float] = fishery

        self.prey: Set[Prey] = set()
        self.predators: Set[Predator] = set()

    @property
    def width(self) -> float:
        return self.size.width

    @property
    def height(self) -> float:
        return self.size.height

    def _count_survivors(self) -> Tuple[int, int]:
        num_prey = sum((prey.children > 0 for prey in self.prey))
        num_predators = sum((predator.children > 0 for predator in self.predators))
        return num_prey, num_predators

    def step(self) -> Tuple[int, int]:
        """
        Move the board forward by one time-step.
        This method also handles the edge case of the first time step.

        :return: numbers of prey and predators that survived the round.
        """
        # Create new set of prey fish
        new_prey = sum((prey.children for prey in self.prey))
        new_prey = min(new_prey, self.prey_capacity)
        if new_prey == 0:
            new_prey = self.starting_prey
        self.prey = set()
        while len(self.prey) < new_prey:
            self.prey.add(Prey(board_size=self.size))

        # Create new set of predator fish
        new_predators = sum((predator.children for predator in self.predators))
        if new_predators == 0:
            new_predators = self.starting_predators
        self.predators = set()
        while len(self.predators) < new_predators:
            self.predators.add(Predator(board_size=self.size))

        # Let the predators feed on the prey
        for predator in self.predators:
            # find all the prey that the predator will eat.
            food: Set[Prey] = set()
            for prey in self.prey:
                if (not prey.got_eaten) and predator.touches(prey):
                    food.add(prey)
            predator.eat(food)

        # apply fishery
        if self.fishery is not None:
            for prey in self.prey:
                if (not prey.got_eaten) and (np.random.uniform() < self.fishery):
                    prey.got_eaten = True

        # adjust the reproduction rate of prey if their population is too close to the carrying capacity
        if len(self.prey) < (self.prey_capacity / (1 + PREY_REPRODUCTION_RATE)):
            reproduction_rate = PREY_REPRODUCTION_RATE
        else:
            reproduction_rate = self.prey_capacity / len(self.prey) - 1

        # Let the fish reproduce
        [prey.reproduce(reproduction_rate) for prey in self.prey]
        [predator.reproduce() for predator in self.predators]

        return self._count_survivors()

    def draw(self) -> Image:
        scale: float = (2 ** 12) // max(self.size)
        image_size = self.width * scale, self.height * scale
        im: Image = Image.new(mode='RGB', size=image_size, color='white')
        draw: ImageDraw = ImageDraw.Draw(im=im)

        [fish.draw(draw, scale) for fish in self.prey]
        [fish.draw(draw, scale) for fish in self.predators]

        num_prey, num_predators = self._count_survivors()
        draw.text(
            xy=(64, 32),
            text=f'Survivors:\nPrey: {num_prey}\nPredators: {num_predators}',
            fill=(0, 255, 0),  # Green text
            font=ImageFont.truetype(font='./arial.ttf', size=64)
        )
        return im
