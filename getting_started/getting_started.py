import numpy as np
from matplotlib import pyplot as plt


def sine_graphs():
    times: np.array = np.arange(25, dtype=float)
    cosine: np.array = np.cos(2 * times / 24 * np.pi)
    sine: np.array = np.sin(2 * times / 24 * np.pi)

    plt.close('all')
    fig = plt.figure(figsize=(8, 4.5), dpi=300)
    ax = fig.add_subplot(111)
    plt.scatter(times, cosine, marker='*', c='red')
    plt.scatter(times, sine, marker='v', c='blue')
    ax.set_xlim([-1, 26])
    ax.set_xlabel('Hour (hr)')
    ax.set_ylim([-1.1, 1.1])
    ax.set_ylabel('cosine (red), sine (blue)')
    plt.savefig('sine_plot.png', bbox_inches='tight', pad_inches=0.25)

    plt.close('all')
    fig = plt.figure(figsize=(6, 6), dpi=300)
    ax = fig.add_subplot(111)
    plt.plot(sine, cosine, marker='o', c='green')

    ax.set_xlim([-1.1, 1.1])
    ax.set_xlabel('sine')

    ax.set_ylim([-1.1, 1.1])
    ax.set_ylabel('cosine')

    plt.savefig('circle_plot.png', bbox_inches='tight', pad_inches=0.25)
    plt.close('all')
    return


if __name__ == '__main__':
    sine_graphs()
