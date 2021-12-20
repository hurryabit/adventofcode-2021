from dataclasses import dataclass
import io

EXAMPLE = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


@dataclass
class Image:
    inner: list[str]
    outer: str


def enhance(algorithm: str, image: Image) -> Image:
    m = len(image.inner)
    n = len(image.inner[0])

    def pixel(i: int, j: int) -> str:
        index = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                index *= 2
                if 0 <= i + di < m and 0 <= j + dj < n:
                    if image.inner[i + di][j + dj] == "#":
                        index += 1
                else:
                    if image.outer == "#":
                        index += 1
        return algorithm[index]

    inner = [
        "".join(pixel(i, j) for j in range(-1, n + 1))
        for i in range(-1, m + 1)
    ]
    outer = algorithm[0] if image.outer == "." else algorithm[511]
    return Image(inner=inner, outer=outer)


def solve(reader: io.TextIOBase) -> int:
    algorithm = reader.readline().strip()
    reader.readline()
    image = Image(
        inner=[line.strip() for line in reader.readlines()],
        outer=".",
    )
    image = enhance(algorithm, enhance(algorithm, image))
    assert image.outer == "."
    return sum(line.count("#") for line in image.inner)


assert solve(io.StringIO(EXAMPLE)) == 35


def main():
    with open("input/day20.txt") as file:
        result = solve(file)
        print(f"{result} pixels are lit")


if __name__ == "__main__":
    main()
