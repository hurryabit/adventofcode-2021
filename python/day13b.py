import io

EXAMPLE = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

EXAMPLE_IMAGE = """#####
#...#
#...#
#...#
#####"""

Dot = tuple[int, int]


def fold_dot(dot: Dot, axis: str, offset: int) -> set[Dot]:
    (x, y) = dot
    if axis == "x":
        return dot if x < offset else (2 * offset - x, y)
    elif axis == "y":
        return dot if y < offset else (x, 2 * offset - y)
    else:
        raise ValueError(f"axis must be 'x' or 'y' but not '{axis}'")


def imagine(dots: set[Dot]) -> str:
    max_x = max(x for (x, _) in dots)
    max_y = max(y for (_, y) in dots)
    matrix = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for (x, y) in dots:
        matrix[y][x] = "#"
    return "\n".join("".join(row) for row in matrix)


def solve(reader: io.TextIOBase) -> str:
    dots = set()
    while (line := reader.readline().strip()) != "":
        [x, y] = line.split(",")
        dots.add((int(x), int(y)))
    for line in reader.readlines():
        [_, _, fold] = line.strip().split()
        [axis, offset] = fold.split("=")
        offset = int(offset)
        dots = {fold_dot(dot, axis, offset) for dot in dots}

    return imagine(dots)


assert solve(io.StringIO(EXAMPLE)) == EXAMPLE_IMAGE


def main():
    with open("input/day13.txt") as file:
        result = solve(file)
        print(result)


if __name__ == "__main__":
    main()
