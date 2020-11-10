# TL;DR

* You need Python3.8 (or later) along with ```numpy```, ```matplotlib```, and ```pillow```.
* You can tweak the default parameters in ```params.py```.
* After that, run ```python3.8 simulate.py``` from the terminal or your IDE.
* Results will be shown as plots in the "simulations" directory.

# Predator-Prey Model

This is my implementation of a predator-prey model tailored to simulate the striper-pogy game we played near the start of the semester.

The ```params.py``` file contains the parameters that can be tweaked.
Take your time changing values as you wish and see how the plots change.

The ```utils.py``` file contains some helper code that I use in the other files.
Note the custom types I defined to capture the concepts of:

* "Size" of the board and fish,
* "Location" of the fish on the board, and
* "Populations" of the species during the simulation.

The ```fish.py``` file contains classes representing the two species of fish.

* The ```Fish``` class captures properties that are common to all fish.
* The ```Prey``` class inherits from the ```Fish``` class and specializes for pogies.
* The ```Predator``` class also inherits from the ```Fish``` class and specializes for stripers.

The ```board.py``` file contains a class representing the game board we used earlier, and the Narragansett Bay in the simulation.
In the ```Board``` class, the ```step``` method handles the logic of a single time-step during the simulation.

* Drop all fish on the board.
* Let the stripers eat the pogies that they overlap.
* Let the surviving fish reproduce for the next time-step.

The ```draw``` method handles the logic for drawing one frame of the animation.
This frame shows everything that happened in that time-step.

* The white background box represents the bay.
* The small blue squares represent pogies.
* The large red squares represent stripers.
* The fish that died are colored gray instead of the usual blue/red.
* The green text near the top-left corner of each frame counts the survivors.

The ```simulate.py``` file contains code that actually uses ```Board```, ```Prey``` and ```Predator``` to run the simulation.

For more details, please read the documentation in the code.
