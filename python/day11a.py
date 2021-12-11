from collections import deque
import io

EXAMPLE = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


Coord = tuple[int, int]


def step(matrix: list[list[int]]) -> int:
    m = len(matrix)
    n = len(matrix)

    def neighbors(coord: Coord) -> list[Coord]:
        (i0, j0) = coord
        return [
            (i, j) for di in [-1, 0, 1] for dj in [-1, 0, 1]
            if (di != 0 or dj != 0) and 0 <= (i := i0 + di) < m and 0 <= (j := j0 + dj) < n
        ]

    flashed = set()
    queue = deque((i, j) for i in range(m) for j in range(n))
    while len(queue) > 0:
        coord = queue.popleft()
        (i, j) = coord
        matrix[i][j] += 1
        if matrix[i][j] > 9 and coord not in flashed:
            flashed.add(coord)
            queue.extend(neighbors(coord))
    for (i, j) in flashed:
        matrix[i][j] = 0
    return len(flashed)


def solve(reader: io.TextIOBase) -> int:
    matrix = []
    for line in reader.readlines():
        matrix.append(list(map(int, line.strip())))
    total_flashes = 0
    for _ in range(100):
        total_flashes += step(matrix)
    return total_flashes


assert solve(io.StringIO(EXAMPLE)) == 1656


def main():
    with open("input/day11.txt") as file:
        result = solve(file)
        print(f"There are {result} total flashes")


if __name__ == "__main__":
    main()
