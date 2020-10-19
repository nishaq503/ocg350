from typing import List

import numpy as np
import streamlit as st
from matplotlib import pyplot as plt


def draw_phase_plot(populations: List[np.array]):
    plt.clf()
    plt.close('all')
    fig = plt.figure(figsize=(8, 8), dpi=128)
    fig.add_subplot(111)

    for run in populations:
        x, y = run[0], run[1]
        plt.quiver(x[:-1], y[:-1], x[1:] - x[:-1], y[1:] - y[:-1],
                   scale_units='xy', angles='xy', scale=1, width=0.0025)

    plt.xlabel('Prey Population')
    plt.ylabel('Predator Population')
    plt.title('Predator-Prey Population Phase Plot')
    st.pyplot(fig)
    return


def main():
    st.title('Predator-Prey Difference Equations')

    prey_capacity = st.slider('Prey Capacity', 50, 200, 75, 5)
    col1, col2 = st.beta_columns(2)
    with col1:
        reproduction_rate = st.slider('Prey Reproduction Rate', 0., 1., 1., 0.05, '%.2f')
        efficiency = st.slider('Ecological Efficiency', 0.05, 0.5, 0.25, 0.05, '%.2f')
        time_steps = st.slider('Time Steps', 10, 250, 100, 10)
    with col2:
        predation_rate = st.slider('Predation Rate', 0.05, 0.4, 0.2, 0.05, '%.2f')
        death_rate = st.slider('Predator Death Rate', 0.05, 0.4, 0.1, 0.05, '%.2f')
        delta_t = st.slider('Step Size', 0.1, 1., 0.25, 0.05, '%.2f')
    grid_size = st.slider('Starting Grid', 0, 20, 0, 2)
    grid_size = grid_size // 2

    starting_prey, starting_predators = 3, 1
    min_prey, min_predators = 3, 1

    def prey_delta(pop_prey, pop_predators):
        delta_pop = pop_prey * (reproduction_rate * (1 - pop_prey / prey_capacity) - predation_rate * pop_predators)
        return max(min(delta_pop * delta_t, prey_capacity - pop_prey), min_prey - pop_prey)

    def predators_delta(pop_prey, pop_predators):
        delta_pop = pop_predators * (predation_rate * efficiency * pop_prey - death_rate * pop_predators)
        return max(delta_pop * delta_t, min_predators - pop_predators)

    def run_simulation(run: np.array):
        for i in range(1, num_steps + 1):
            prev_prey, prev_predators = run[0, i - 1], run[1, i - 1]
            next_prey = prev_prey + prey_delta(prev_prey, prev_predators)
            next_predators = prev_predators + predators_delta(prev_prey, prev_predators)
            run[:, i] = (next_prey, next_predators)
        return run

    num_steps = int(time_steps / delta_t)
    first_run = np.zeros((2, num_steps + 1), dtype=float)
    first_run[:, 0] = (starting_prey, starting_predators)
    first_run = run_simulation(first_run)
    populations: List[np.array] = [first_run]

    if grid_size > 0:
        max_prey, max_predators = max(first_run[0]), max(first_run[1])
        prey_step, predators_step = (max_prey - min_prey) / grid_size, (max_predators - min_predators) / grid_size
        for x in range(1, 1 + grid_size):
            for y in range(1, 1 + grid_size):
                starting_prey = min_prey + prey_step * (x - 0.5 * (y % 2))
                starting_predators = min_predators + predators_step * (y + 0.5 * (x % 2))
                new_run = np.zeros_like(first_run)
                new_run[:, 0] = (starting_prey, starting_predators)
                new_run = run_simulation(new_run)
                populations.append(new_run)

    draw_phase_plot(populations)
    return


if __name__ == '__main__':
    main()
