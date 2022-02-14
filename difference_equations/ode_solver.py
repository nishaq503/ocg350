from typing import Tuple, List

import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
from scipy.integrate import odeint

from app import draw_phase_plot, get_isoclines


def draw_time_series(populations: List[np.array], times: np.array):
    plt.clf()
    fig = plt.figure(figsize=(8, 5), dpi=128)
    fig.add_subplot(111)

    for run in populations:
        plt.plot(times, run[0], c='blue', label='Prey Population', lw=0.75)
        plt.plot(times, run[1], c='red', label='Predator Population', lw=0.75)

    plt.xlabel('Time')
    plt.ylabel('Populations')
    plt.title('Prey (Blue) and Predators (red) vs time')
    st.pyplot(fig)
    return


def main():
    st.title('Predator-Prey Differential Equations')

    prey_capacity = st.slider('Prey Capacity', 50, 200, 100, 5)
    col1, col2 = st.columns(2)
    with col1:
        reproduction_rate = st.slider('Prey Reproduction Rate', 0., 1., 0.5, 0.05, '%.2f')
        efficiency = st.slider('Ecological Efficiency', 0.05, 0.4, 0.15, 0.01, '%.2f')
    with col2:
        consumption_rate = st.slider('Consumption Rate', 0.01, 0.2, 0.05, 0.01, '%.2f')
        death_rate = st.slider('Predator Death Rate', 0.01, 0.2, 0.05, 0.01, '%.2f')
    grid_size = st.slider('Starting Grid', 0, 20, 0, 2)
    grid_size = grid_size // 2

    min_prey, min_predators = 3, 1

    def solve(initial: Tuple[float, float], time: np.array) -> np.array:

        def differential(_p: np.array, _) -> Tuple[float, float]:
            [num_pogies, num_stripers] = list(_p)

            pogies_delta = num_pogies * (reproduction_rate * (1 - num_pogies / prey_capacity) - consumption_rate * num_stripers)
            pogies_delta = max(pogies_delta, 3 - num_pogies)

            stripers_delta = num_stripers * (efficiency * consumption_rate * num_pogies - death_rate * num_stripers)
            stripers_delta = max(stripers_delta, 1 - num_stripers)
            return pogies_delta, stripers_delta

        return np.asarray(odeint(differential, initial, time)).T

    time_steps = np.arange(start=0, stop=100, step=0.25)
    first_run = solve((3, 1), time_steps)
    populations: List[np.array] = [first_run]

    if grid_size > 0:
        max_prey, max_predators = max(first_run[0]), max(first_run[1])
        prey_step, predators_step = (max_prey - min_prey) / grid_size, (max_predators - min_predators) / grid_size
        for x in range(1, 1 + grid_size):
            for y in range(1, 1 + grid_size):
                starting_prey = min_prey + prey_step * (x - 0.5 * (y % 2))
                starting_predators = min_predators + predators_step * (y + 0.5 * (x % 2))
                new_run = solve((starting_prey, starting_predators), time_steps)
                populations.append(new_run)

    constants = [reproduction_rate, prey_capacity, consumption_rate, efficiency, death_rate]
    isoclines = get_isoclines((min(first_run[0]), max(first_run[0])), *constants)
    st.write(f'The Equilibrium populations are: prey: {first_run[0][-1]:.1f}, predators: {first_run[1][-1]:.1f}')

    draw_time_series(populations, time_steps)
    draw_phase_plot(populations, isoclines)
    return


if __name__ == '__main__':
    main()
