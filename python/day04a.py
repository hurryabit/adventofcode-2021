import io
from collections.abc import Iterable
from typing import Optional

EXAMPLE = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


Board = list[list[Optional[int]]]


def parse(reader: io.TextIOBase) -> tuple[list[int], list[Board]]:
    numbers = list(map(int, reader.readline().strip().split(",")))
    boards = []
    while True:
        line0 = reader.readline()
        if not line0:
            break
        board: Board = []
        for _ in range(5):
            board.append(list(map(int, reader.readline().strip().split())))
        boards.append(board)
    return (numbers, boards)


def call(board: Board, number: int) -> bool:
    def has_complete_row(iter: Iterable[Iterable[Optional[int]]]) -> bool:
        return any(all(cell is None for cell in row) for row in iter)

    for (i, row) in enumerate(board):
        for (j, cell) in enumerate(row):
            if cell == number:
                board[i][j] = None
    return has_complete_row(board) or has_complete_row(zip(*board))


def score(board: Board) -> int:
    return sum(cell for row in board for cell in row if cell is not None)


def solve(reader: io.TextIOBase) -> Optional[int]:
    (numbers, boards) = parse(reader)

    for number in numbers:
        for board in boards:
            if call(board, number):
                return score(board) * number
    return None


assert solve(io.StringIO(EXAMPLE)) == 4512


def main():
    with open("input/day04.txt") as file:
        result = solve(file)
        print(f"The final score will be {result}")


if __name__ == "__main__":
    main()
