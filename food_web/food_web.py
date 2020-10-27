import os
from typing import List, Dict, Optional

from matplotlib import pyplot as plt
import numpy as np
from scipy.linalg import solve

PARTICIPANTS: List[str] = [
    'Sun',
    'Phytoplankton',
    'Zooplankton',
    'Copepod',
    'Shrimp',
    'Lobster',
    'Lantern',
    'Squid',
    'Tuna',
    'Marlin',
    'Shark',
]


FOOD_WEB: Dict[str, Dict[str, float]] = {
    'Sun': {'Phytoplankton': 1.},
    'Phytoplankton': {'Zooplankton': .5, 'Copepod': .3, 'Shrimp': .2},
    'Zooplankton': {'Zooplankton': .2, 'Copepod': .3, 'Shrimp': .3, 'Lobster': .2},
    'Copepod': {'Copepod': .2, 'Lobster': .5, 'Lantern': .3},
    'Shrimp': {'Shrimp': .1, 'Lobster': .4, 'Tuna': .5},
    'Lobster': {'Tuna': .5, 'Marlin': .5},
    'Lantern': {'Squid': 1.},
    'Squid': {'Tuna': .4, 'Marlin': .3, 'Shark': .3},
    'Tuna': {'Marlin': .5, 'Shark': .5},
    'Marlin': {'Shark': 1.},
    'Shark': {'Shark': 1.},
}


EFFICIENCY: Dict[str, float] = {
    'Phytoplankton': .9,
    'Zooplankton': .3,
    'Copepod': .25,
    'Shrimp': .2,
    'Lobster': .2,
    'Lantern': .15,
    'Squid': .12,
    'Tuna': .1,
    'Marlin': .1,
    'Shark': .1,
}


HUMAN = ['Shrimp', 'Lobster', 'Tuna', 'Marlin']


def check_web():
    assert len(PARTICIPANTS) == len(FOOD_WEB), f'mismatch: {len(PARTICIPANTS)}, {len(FOOD_WEB)}'
    assert len(PARTICIPANTS) == len(EFFICIENCY) + 1, f'mismatch: {len(PARTICIPANTS)}, {len(EFFICIENCY) + 1}'
    for participant in PARTICIPANTS:
        assert participant in FOOD_WEB, f'PARTICIPANT {participant} not found in FOOD_WEB'
        if participant == 'Sun':
            continue
        else:
            assert participant in EFFICIENCY, f'PARTICIPANT {participant} not found in EFFICIENCY'

    for source, consumers in FOOD_WEB.items():
        for consumer in consumers:
            assert consumer in PARTICIPANTS, f'consumer {consumer} not found in PARTICIPANTS'
        if source == 'Human':
            continue
        else:
            assert sum(consumers.values()) == 1., f'total consumption fraction different different from 1. for {source}'
    return


def solve_food_web(
        input_flux: float,
        *,
        include_humans: bool = True,
        latex: Optional[str] = None,
        draw: Optional[str] = None,
) -> np.array:
    if include_humans:
        PARTICIPANTS.append('Human')
        EFFICIENCY['Human'] = 0.1
        FOOD_WEB['Human'] = dict()
        for source in HUMAN:
            consumers = {c: v / 2 for c, v in FOOD_WEB[source].items()}
            consumers['Human'] = 0.5
            FOOD_WEB[source] = consumers

    check_web()
    enumeration: Dict[str, int] = {p: i for i, p in enumerate(PARTICIPANTS[1:])}

    # create matrix to store constants
    diet_matrix: np.ndarray = np.zeros(shape=(len(EFFICIENCY), len(EFFICIENCY)))
    for source, consumers in FOOD_WEB.items():
        if source == 'Sun':
            continue
        else:
            j = enumeration[source]
            for consumer, fraction in consumers.items():
                i = enumeration[consumer]
                diet_matrix[i, j] = -fraction

    if draw:
        # draw food web using graphviz
        pass

    for col in range(diet_matrix.shape[0] - 1):
        assert sum(diet_matrix[:, col]) == -1, f'consumption fractions did not sum to -1'

    for participant, i in enumeration.items():
        diet_matrix[i, i] = 1 / EFFICIENCY[participant]

    constants: np.array = np.zeros(len(EFFICIENCY))
    constants[0] = input_flux
    solution = solve(diet_matrix, constants)

    if latex is not None:
        # TODO: print equation as lAtEx
        pass
    return solution


def plot_bar_chart(with_humans: np.array, without_humans: np.array, title: str, filename: str):
    without_humans = list(without_humans)
    without_humans.append(0)

    x = np.arange(start=0, stop=len(with_humans))

    fig = plt.figure(figsize=(16, 10), dpi=200)
    ax = fig.add_subplot(111)
    plt.bar(x - .21, without_humans, align='center', log=True, width=.4, color='blue')
    plt.bar(x + .21, with_humans, align='center', log=True, width=.4, color='red')

    ax.set_xticks(range(len(PARTICIPANTS) - 1))
    ax.set_xticklabels(PARTICIPANTS[1:], rotation=45)

    plt.xlabel('Participants', fontsize=16)
    plt.ylabel('Fraction', fontsize=16)

    plt.title(title, fontsize=24)
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.25)
    plt.close('all')
    return


if __name__ == '__main__':
    _filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bar_plots.png'))
    _without_humans = solve_food_web(1_160, include_humans=False)
    _with_humans = solve_food_web(1_160, include_humans=True)
    plot_bar_chart(_with_humans, _without_humans, 'Food Web with (red) and without (blue) Humans', _filename)
