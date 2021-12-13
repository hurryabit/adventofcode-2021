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


Dot = tuple[int, int]


def fold_dot(dot: Dot, axis: str, offset: int) -> set[Dot]:
    (x, y) = dot
    if axis == "x":
        return dot if x < offset else (2 * offset - x, y)
    elif axis == "y":
        return dot if y < offset else (x, 2 * offset - y)
    else:
        raise ValueError(f"axis must be 'x' or 'y' but not '{axis}'")


def solve(reader: io.TextIOBase) -> int:
    dots = set()
    while (line := reader.readline().strip()) != "":
        [x, y] = line.split(",")
        dots.add((int(x), int(y)))
    line = reader.readline().strip()
    [_, _, fold] = line.split()
    [axis, offset] = fold.split("=")
    offset = int(offset)
    dots_after_fold = {fold_dot(dot, axis, offset) for dot in dots}
    return len(dots_after_fold)


assert solve(io.StringIO(EXAMPLE)) == 17


def main():
    with open("input/day13.txt") as file:
        result = solve(file)
        print(f"{result} dots are visible")


if __name__ == "__main__":
    main()
