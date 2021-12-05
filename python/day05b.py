import io
import math
from dataclasses import dataclass, replace
from typing import Iterator

EXAMPLE = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


def sign(n: int) -> int:
    return 0 if n == 0 else int(math.copysign(1, n))


assert sign(0) == 0
assert sign(1) == 1
assert sign(2) == 1
assert sign(-1) == -1
assert sign(-2) == -1


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    @staticmethod
    def parse(input: str):
        [x, y] = input.split(",")
        return Point(x=int(x), y=int(y))

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __rmul__(self, scalar):
        return Point(scalar * self.x, scalar * self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def unit(self):
        return Point(sign(self.x), sign(self.y))

    def l_inf(self):
        return max(abs(self.x), abs(self.y))


assert 2 * Point(1, 1) == Point(2, 2)


def det(col1: Point, col2: Point) -> int:
    return col1.x * col2.y - col2.x * col1.y


assert det(Point(1, 2), Point(3, 4)) == -2


@dataclass
class Segment:
    start: Point
    dir: Point
    len: int

    @staticmethod
    def parse(input: str):
        [start_str, _, end_str] = input.strip().split()
        start = Point.parse(start_str)
        end = Point.parse(end_str)
        if start > end:
            (start, end) = (end, start)
        delta = end - start
        return Segment(start=start, dir=delta.unit(), len=delta.l_inf())

    def __str__(self) -> str:
        return f"[{self.start} + (0..{len(self)}) * {self.dir}]"

    @property
    def end(self):
        return self.start + len(self) * self.dir

    def __len__(self):
        return self.len

    def __call__(self, **kwargs):
        return replace(self, **kwargs)

    def __getitem__(self, k: int) -> Point:
        return self.start + k * self.dir

    def __iter__(self) -> Iterator[Point]:
        return (self[k] for k in range(0, len(self) + 1))

    def __contains__(self, point: Point) -> bool:
        dist = (point - self.start).l_inf()
        return dist <= len(self) and self.start + dist * self.dir == point

    def __and__(self, other):
        if self.dir == other.dir:
            if self.start in other:
                length = min((other.end - self.start).l_inf(), len(self))
                return self(len=length)
            elif other.start in self:
                length = min((self.end - other.start).l_inf(), len(other))
                return other(len=length)
            else:
                return None
        else:
            delta = other.start - self.start
            k = det(delta, -other.dir) // det(self.dir, -other.dir)
            point = self[k]
            return point if point in self and point in other else None


def solve(reader: io.TextIOBase) -> int:
    segments = []
    for line in reader.readlines():
        segment = Segment.parse(line)
        segments.append(segment)

    result = set()
    for (i, segment1) in enumerate(segments):
        for j in range(i + 1, len(segments)):
            segment2 = segments[j]
            intersection = segment1 & segment2
            if isinstance(intersection, Point):
                result.add(intersection)
            elif isinstance(intersection, Segment):
                result.update(set(intersection))
            else:
                assert intersection is None
    return len(result)


assert solve(io.StringIO(EXAMPLE)) == 12


def main():
    with open("input/day05.txt") as file:
        result = solve(file)
        print(f"There are {result} points of overlap")


if __name__ == "__main__":
    main()
