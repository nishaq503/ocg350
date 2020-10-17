from typing import List

import numpy as np
import streamlit as st
from matplotlib import pyplot as plt


def draw_phase_plot(populations: List[np.array]):
    plt.clf()
    plt.close('all')
    fig = plt.figure(figsize=(12, 12), dpi=200)
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

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        size = st.slider('Board Size', 1, 10, 5, 1)
        prey_reproduction_rate = st.slider('Prey Reproduction Rate', 0., 1., 0.75, 0.01)
    with col2:
        prey_size = st.slider('Prey size', 0.1, 3., 2., 0.1, '%.1f')
        predator_food_requirement = st.slider('Predator Food Requirement', 1., 5., 1.5, 0.1, '%.1f')
    with col3:
        predator_size = st.slider('Predator size', 1., 10., 5., 0.1, '%.1f')
        fishing_rate = st.slider('Fishing Rate', 0., 1., 0.2, 0.01)

    col1, col2 = st.beta_columns(2)
    with col1:
        time_steps = st.slider('Time Steps', 10, 250, 100, 10)
    with col2:
        delta_t = st.slider('Step Size', 0.1, 1., 0.25, 0.05)

    board_size = 16 * size
    prey_capacity = 75 * size * size
    starting_prey, starting_predators = 3, 1
    min_prey, min_predators = 3, 1

    prey_margin = (board_size - prey_size) ** 2
    predator_margin = (board_size - predator_size) ** 2
    predator_prey_area = (predator_size + prey_size) ** 2
    predator_predator_area = (predator_size * 2) ** 2
    predator_prey_overlap = predator_prey_area / prey_margin
    predator_predator_overlap = predator_predator_area / predator_margin

    def next_pop_prey(pop_prey: float, pop_predators: float) -> float:
        if pop_prey < prey_capacity / (1 + prey_reproduction_rate):
            reproduction_rate = prey_reproduction_rate
        else:
            reproduction_rate = prey_capacity / pop_prey - 1
        survival_rate = (1 - predator_prey_overlap) ** pop_predators
        next_pop = (1 + reproduction_rate) * survival_rate * (1 - fishing_rate) * pop_prey
        pop_delta = delta_t * (next_pop - pop_prey)
        pop_delta = max(min(pop_delta, prey_capacity - pop_prey), min_prey - pop_prey)
        return pop_prey + pop_delta

    def next_pop_predators(pop_prey: float, pop_predators: float) -> float:
        num_eaten = pop_prey * (1 - (1 - predator_prey_overlap) ** pop_predators)
        self_competition = ((1 - predator_predator_overlap) ** pop_predators)
        next_pop = (num_eaten / predator_food_requirement) * self_competition
        pop_delta = delta_t * (next_pop - pop_predators)
        pop_delta = max(pop_delta, min_predators - pop_predators)
        return pop_predators + pop_delta

    def run_simulation(run: np.array):
        for i in range(1, num_steps + 1):
            prev_prey, prev_predators = run[0, i - 1], run[1, i - 1]
            next_prey = next_pop_prey(prev_prey, prev_predators)
            next_predators = next_pop_predators(prev_prey, prev_predators)
            run[:, i] = (next_prey, next_predators)
        return run

    num_steps = int(time_steps / delta_t)
    first_run = np.zeros((2, num_steps + 1), dtype=float)
    first_run[:, 0] = (starting_prey, starting_predators)
    first_run = run_simulation(first_run)
    populations: List[np.array] = [first_run]

    stable_prey, stable_predators = first_run[0, -1], first_run[1, -1]
    stable_prey, stable_predators = max(stable_prey, 100), max(stable_predators, 10)
    grid_size = 4
    prey_step = (stable_prey - min_prey) / grid_size
    predators_step = (stable_predators - min_predators) / grid_size
    for x in range(1, 1 + 2 * grid_size):
        for y in range(1, 1 + 2 * grid_size):
            starting_prey = min_prey + prey_step * (x + 0.5 * (y % 2))
            starting_predators = min_predators + predators_step * y
            new_run = np.zeros_like(first_run)
            new_run[:, 0] = (starting_prey, starting_predators)
            new_run = run_simulation(new_run)
            populations.append(new_run)

    draw_phase_plot(populations)
    return


if __name__ == '__main__':
    main()
