from typing import Set, Tuple

import numpy as np

from fish import Fish, Predator, Prey
from utils import Size, Location


class Board:
    def __init__(
            self,
            size: Size,
            prey_capacity: int = np.inf,
            prey_injection: int = 3,
            predator_capacity: int = np.inf,
            predator_injection: int = 1,
    ):
        """
        Initializes a board with a given size.

        :param size: (width, height) of board to use.
        """
        self.size: Size = size

        self.predator_capacity: int = predator_capacity
        self.predator_injection: int = predator_injection
        self.predators: Set[Predator] = set()

        self.prey_capacity: int = prey_capacity
        self.prey_injection: int = prey_injection
        self.prey: Set[Prey] = set()

    @property
    def width(self) -> float:
        return self.size.width

    @property
    def height(self) -> float:
        return self.size.height

    def _drop(self, fish: Fish):
        """
        Helper method for dropping a fish on the board.

        :param fish: to be dropped.
        :return: nothing.
        """
        def sample(margin: float, length: float) -> float:
            """ Uniform random sample over length, excluding margin from each end. """
            return np.random.uniform(low=margin, high=length - margin)

        x: float = sample(fish.width / 2, self.width)
        y: float = sample(fish.height / 2, self.height)
        fish.location = Location(x, y)
        return

    def drop_fish(self, fishes: Set[Fish]) -> 'Board':
        """
        Drops the given set of fish on the board.

        If the fishes are predators, let them eat after dropping.
        A predator eats a prey if they touch each other.

        :param fishes: set of fish to add to the board.
        :return: returns the updated board.
        """
        for fish in fishes:
            self._drop(fish)
            if isinstance(fish, Predator):  # if the fish is a predator,
                # find all the prey that the predator will eat.
                food: Set[Prey] = set()
                for prey in self.prey:
                    if (not prey.got_eaten) and fish.touches(prey):
                        food.add(prey)
                fish.eat(food)

        return self

    def _count_survivors(self) -> Tuple[int, int]:
        num_prey = sum((prey.children > 0 for prey in self.prey))
        num_predators = sum((predator.children > 0 for predator in self.predators))
        return num_prey, num_predators

    def start(
            self,
            num_prey: int,
            num_predators: int,
    ) -> Tuple[int, int]:
        """
        Get the board started with the given populations of predators and prey.

        :param num_prey: number of prey to start with.
        :param num_predators: number of predators to start with.
        :return: numbers of prey and predators that survived the first round.
        """
        self.prey = {Prey() for _ in range(num_prey)}
        self.drop_fish(self.prey)

        self.predators = {Predator() for _ in range(num_predators)}
        self.drop_fish(self.predators)

        return self._count_survivors()

    def step(self) -> Tuple[int, int]:
        """
        Move the board forward by one time-step.

        :return: numbers of prey and predators that survived the round.
        """
        new_prey = sum((prey.children for prey in self.prey))
        new_prey = max(self.prey_injection, min(new_prey, self.prey_capacity))
        self.prey = {Prey() for _ in range(new_prey)}
        self.drop_fish(self.prey)

        new_predators = sum((predator.children for predator in self.predators))
        new_predators = max(self.predator_injection, min(new_predators, self.predator_capacity))
        self.predators = {Predator() for _ in range(new_predators)}
        self.drop_fish(self.predators)

        [prey.reproduce() for prey in self.prey]
        [predator.reproduce() for predator in self.predators]

        return self._count_survivors()
