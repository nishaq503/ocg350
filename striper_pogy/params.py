from utils import Size

# change this to change the area of the board and proportionally change the carrying capacity of prey
SIZE_MULTIPLIER = 1

# dimensions of the board
BOARD_SIZE: Size = Size(17 * SIZE_MULTIPLIER, 11 * SIZE_MULTIPLIER)

# size of canvas to use for drawing the animation. DO NOT CHANGE this without understanding the cascading effects.
CANVAS_SCALE = (2 ** 12) // max(BOARD_SIZE)

PREY_SIZE: Size = Size(1, 1)
PREY_CAPACITY: int = 75 * (SIZE_MULTIPLIER ** 2)
PREY_REPRODUCTION_RATE: float = 0.5
STARTING_PREY = 3

PREDATOR_SIZE: Size = Size(2.5, 2.5)
STARTING_PREDATORS = 1

# number of prey that need to be eaten to let stripers to survive and (maybe) reproduce.
# e.g. with default value of 3, predator survives with 3, reproduces once with 6, reproduces twice with 9, and so on.
PREDATOR_FOOD_REQUIREMENTS: int = 3

# Number of times to run the simulation
NUM_SIMULATIONS = 1

# number of time steps for which to run each simulation
TIME_STEPS = 128

# whether to erase old plots before generating new ones when rerunning code
ERASE = True

# whether to use the first simulation to create an animation of the model
ANIMATE = False
