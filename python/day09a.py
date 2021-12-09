import io

EXAMPLE = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def solve(reader: io.TextIOBase) -> int:
    matrix: list[list[int]] = []
    for line in reader.readlines():
        matrix.append(list(map(int, line.strip())))
    m = len(matrix)
    n = len(matrix[0])
    result = 0
    for (i, row) in enumerate(matrix):
        for (j, cell) in enumerate(row):
            is_low_point = all(
                cell < matrix[i + di][j + dj]
                for (di, dj) in [(-1, 0), (0, -1), (0, 1), (1, 0)]
                if 0 <= i + di < m and 0 <= j + dj < n
            )
            if is_low_point:
                result += cell + 1
    return result


assert solve(io.StringIO(EXAMPLE)) == 15


def main():
    with open("input/day09.txt") as file:
        result = solve(file)
        print(f"The total risk level is {result}")


if __name__ == "__main__":
    main()
