import io
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


class Board:
    table: dict[int, tuple[set[int], set[int]]]

    def __init__(self, data: list[list[int]]):
        rows = [set(row) for row in data]
        cols = [set(col) for col in zip(*data)]
        row_table = {}
        for row in rows:
            for cell in row:
                row_table[cell] = row
        table = {}
        for col in cols:
            for cell in col:
                table[cell] = (row_table[cell], col)
        self.table = table

    def call(self, number: int) -> bool:
        if number in self.table:
            (row, col) = self.table[number]
            del self.table[number]
            row.remove(number)
            col.remove(number)
            if not row or not col:
                return True

        return False

    def score(self) -> int:
        return sum(self.table)


def parse(reader: io.TextIOBase) -> tuple[list[int], list[Board]]:
    numbers = list(map(int, reader.readline().strip().split(",")))
    boards = []
    while True:
        line0 = reader.readline()
        if not line0:
            break
        board = []
        for _ in range(5):
            board.append(list(map(int, reader.readline().strip().split())))
        boards.append(Board(board))
    return (numbers, boards)


def solve(reader: io.TextIOBase) -> Optional[int]:
    (numbers, boards) = parse(reader)

    for number in numbers:
        open_boards = [board for board in boards if not board.call(number)]
        if not open_boards:
            return boards[0].score() * number
        boards = open_boards
    return None


assert solve(io.StringIO(EXAMPLE)) == 1924


def main():
    with open("input/day04.txt") as file:
        result = solve(file)
        print(f"The final score will be {result}")


if __name__ == "__main__":
    main()
