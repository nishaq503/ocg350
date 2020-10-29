import os
from typing import List, Dict

import numpy as np
from matplotlib import pyplot as plt
from scipy.linalg import solve

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

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


def _create_dotfile():
    name: str = 'with_humans' if 'Human' in PARTICIPANTS else 'without_humans'
    digraph: List[str] = [f'digraph {name}' + ' {']
    for source, consumers in FOOD_WEB.items():
        for consumer, fraction in consumers.items():
            digraph.append(f'{source} -> {consumer} [label={fraction:.2f}];')
    digraph.append('}')
    dot_string: str = '\n'.join(digraph)

    dot_file: str = os.path.join(BASE_DIR, f'{name}.dot')
    with open(dot_file, 'w') as fp:
        fp.write(dot_string)

    png_file: str = os.path.join(BASE_DIR, f'{name}.png')
    os.system(f'dot -Tpng {dot_file} -o {png_file}')
    os.remove(dot_file)
    return


def _write_latex(diet_matrix: np.array):
    lines: List[str] = ['\\begin{bmatrix}']
    for row in diet_matrix:
        lines.append('    ' + ' & '.join([f'{v:.2f}' for v in row]) + ' \\\\')
    else:
        lines[-1] = lines[-1][:-3]
        lines.append('\\end{bmatrix}')

    matrix: str = '\n'.join(lines)
    name: str = 'with_humans' if 'Human' in PARTICIPANTS else 'without_humans'
    with open(os.path.join(BASE_DIR, f'{name}.txt'), 'w') as fp:
        fp.write(matrix)
    return


def solve_food_web(
        *,
        input_flux: float,
        include_humans: bool,
        latex: bool = True,
        draw_web: bool = True,
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

    if draw_web:
        _create_dotfile()

    for col in range(diet_matrix.shape[0] - 1):
        assert sum(diet_matrix[:, col]) == -1, f'consumption fractions did not sum to -1'

    for participant, i in enumeration.items():
        diet_matrix[i, i] = 1 / EFFICIENCY[participant]

    constants: np.array = np.zeros(len(EFFICIENCY))
    constants[0] = input_flux
    solution = solve(diet_matrix, constants)

    if latex:
        _write_latex(diet_matrix)
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
    plt.ylabel('Consumption (gC m^-2 yr^-1)', fontsize=16)

    plt.title(title, fontsize=24)
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.25)
    plt.close('all')
    return


if __name__ == '__main__':
    _filename = os.path.join(BASE_DIR, 'bar_plots.png')
    _without_humans = solve_food_web(input_flux=690, include_humans=False)
    _with_humans = solve_food_web(input_flux=690, include_humans=True)
    plot_bar_chart(_with_humans, _without_humans, 'Food Web with (red) and without (blue) Humans', _filename)
