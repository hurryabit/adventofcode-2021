import io
from typing import Iterator

EXAMPLE = """2199943210
3987894921
9856789892
8767896789
9899965678"""

Coord = tuple[int, int]


def solve(reader: io.TextIOBase) -> int:
    matrix: list[list[int]] = []
    for line in reader.readlines():
        matrix.append(list(map(int, line.strip())))
    m = len(matrix)
    n = len(matrix[0])

    def neighbors(coord: Coord) -> Iterator[Coord]:
        (i0, j0) = coord
        if matrix[i0][j0] == 9:
            return
        for (di, dj) in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            (i, j) = (i0 + di, j0 + dj)
            if 0 <= i < m and 0 <= j < n and matrix[i][j] != 9:
                yield (i, j)

    seen = set()

    def dfs(coord) -> None:
        if coord in seen:
            return
        seen.add(coord)
        for neighbor in neighbors(coord):
            dfs(neighbor)

    basin_sizes = []
    for i in range(m):
        for j in range(n):
            coord = (i, j)
            if matrix[i][j] != 9 and coord not in seen:
                seen_size = len(seen)
                dfs(coord)
                basin_sizes.append(len(seen) - seen_size)
    basin_sizes.sort(reverse=True)
    [size0, size1, size2] = basin_sizes[:3]
    return size0 * size1 * size2


assert solve(io.StringIO(EXAMPLE)) == 1134


def main():
    with open("input/day09.txt") as file:
        result = solve(file)
        print(f"The sizes of the three largest basins multiply to {result}")


if __name__ == "__main__":
    main()
