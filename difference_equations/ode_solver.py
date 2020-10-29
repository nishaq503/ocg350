from typing import Tuple

import numpy as np
from scipy.integrate import odeint

from matplotlib import pyplot as plt

R = 1.0
K = 100
E = 0.2
C = 0.1
D = 0.05


def solve(initial: Tuple[float, float], time: np.array) -> np.array:

    def differential(populations: np.array, _) -> Tuple[float, float]:
        [num_pogies, num_stripers] = list(populations)

        pogies_delta = num_pogies * (R * (1 - num_pogies / K) - C * num_stripers)
        pogies_delta = max(pogies_delta, 3 - num_pogies)

        stripers_delta = num_stripers * (E * C * num_pogies - D * num_stripers)
        stripers_delta = max(stripers_delta, 1 - num_stripers)

        return pogies_delta, stripers_delta

    return odeint(differential, initial, time)


def main():
    initial = 3, 1
    delta_t = 4
    time = [t / 4 for t in range(100 * delta_t + 1)]
    populations = np.asarray(solve(initial, time))

    fig = plt.figure(figsize=(8, 5), dpi=200)
    fig.add_subplot(111)

    plt.plot(time, populations, lw=0.75)

    plt.xlabel('Time (s)')
    plt.ylabel('Populations')
    plt.legend(['pogies', 'stripers'])
    plt.title('Population vs Time of stripers and pogies from odeint')
    plt.savefig('odeint_solution.png', bbox_inches='tight', pad_inches=0.25)
    plt.close(fig)
    return


if __name__ == '__main__':
    main()
