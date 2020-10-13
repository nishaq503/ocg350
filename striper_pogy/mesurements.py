from board import Board
from fish import Predator, Prey


def predator_prey_overlap():
    board: Board = Board()
    overlaps, n = 0, 1_000_000

    for _ in range(n):
        predator, prey = Predator(board.size), Prey(board.size)
        if predator.touches(prey):
            overlaps += 1

    p = overlaps / n
    print(f'{p:.6f}')

    for _ in range(n):
        predator, prey = Predator(board.size), Prey(board.size)
        if predator.touches(prey):
            overlaps += 1

    q = overlaps / n
    print(f'{q:.6f}')

    return


if __name__ == '__main__':
    predator_prey_overlap()
