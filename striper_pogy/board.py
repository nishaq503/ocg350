from typing import Set, Tuple

from PIL import Image, ImageDraw, ImageFont

from fish import Predator, Prey
from params import *
from utils import Size


class Board:
    def __init__(
            self,
            *,  # all arguments after a * must be passed by name.
            size: Size = BOARD_SIZE,
            starting_prey: int = STARTING_PREY,
            prey_capacity: int = PREY_CAPACITY,
            starting_predators: int = STARTING_PREDATORS,
    ):
        """
        Initializes a board with a given size.

        :param size: (width, height) of board to use.
        :param starting_prey: number of prey with which to start a simulation.
        :param prey_capacity: carrying capacity of the prey.
        :param starting_predators: number of predators with which to start a simulation.
        """
        self.size: Size = size

        self.starting_prey = starting_prey
        self.predators: Set[Predator] = set()

        self.starting_predators = starting_predators
        self.prey_capacity: int = prey_capacity
        self.prey: Set[Prey] = set()

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
        self.prey = {Prey(board_size=self.size) for _ in range(new_prey)}

        # Create new set of predator fish
        new_predators = sum((predator.children for predator in self.predators))
        if new_predators == 0:
            new_predators = self.starting_predators
        self.predators = {Predator(board_size=self.size) for _ in range(new_predators)}

        # Let predators feed on fish
        for predator in self.predators:
            # find all the prey that the predator will eat.
            food: Set[Prey] = set()
            for prey in self.prey:
                if (not prey.got_eaten) and predator.touches(prey):
                    food.add(prey)
            predator.eat(food)

        # adjust the reproduction rate of prey if their population is too close to the carrying capacity
        if len(self.prey) < self.prey_capacity / (1 + PREY_REPRODUCTION_RATE):
            reproduction_rate = PREY_REPRODUCTION_RATE
        else:
            reproduction_rate = self.prey_capacity / len(self.prey) - 1

        # Let the fish reproduce
        [prey.reproduce(reproduction_rate) for prey in self.prey]
        [predator.reproduce() for predator in self.predators]

        return self._count_survivors()

    def draw(self, scale: float = CANVAS_SCALE) -> Image:
        image_size = self.width * scale, self.height * scale
        im: Image = Image.new(mode='RGB', size=image_size, color='white')
        draw: ImageDraw = ImageDraw.Draw(im=im)

        [fish.draw(draw, scale) for fish in self.prey]
        [fish.draw(draw, scale) for fish in self.predators]

        num_prey, num_predators = self._count_survivors()
        draw.text(
            xy=(64, 32),
            text=f'prey: {num_prey}\npredators: {num_predators}',
            fill=(0, 255, 0),
            font=ImageFont.truetype(font='./arial.ttf', size=48)
        )

        return im
