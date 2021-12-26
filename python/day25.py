import io

EXAMPLE = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""


def step(map: list[list[str]]) -> bool:
    m = len(map)
    n = len(map[0])
    move_east = set()
    for i in range(m):
        for j in range(n):
            if map[i][j] == ">" and map[i][(j + 1) % n] == ".":
                move_east.add((i, j))
    for (i, j) in move_east:
        map[i][j] = "."
        map[i][(j + 1) % n] = ">"
    move_south = set()
    for i in range(m):
        for j in range(n):
            if map[i][j] == "v" and map[(i + 1) % m][j] == ".":
                move_south.add((i, j))
    for (i, j) in move_south:
        map[i][j] = "."
        map[(i + 1) % m][j] = "v"
    return len(move_east) > 0 or len(move_south) > 0


def solve(reader: io.TextIOBase) -> int:
    map = []
    for line in reader.readlines():
        map.append(list(line.strip()))
    result = 1
    while step(map):
        result += 1
    return result


assert solve(io.StringIO(EXAMPLE)) == 58


def main():
    with open("input/day25.txt") as file:
        result = solve(file)
        print(f"On step {result} nobody moves")


if __name__ == "__main__":
    main()
