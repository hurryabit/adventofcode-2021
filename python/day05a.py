import io
from dataclasses import dataclass
from enum import Enum

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


class Dir(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @staticmethod
    def parse(input: str):
        [x, y] = input.split(",")
        return Point(x=int(x), y=int(y))


@dataclass
class Segment:
    dir: Dir
    start: Point
    end: Point

    @staticmethod
    def parse(input: str):
        [q1, _, q2] = input.strip().split()
        p1 = Point.parse(q1)
        p2 = Point.parse(q2)
        if p1.x == p2.x:
            (start, end) = (p1, p2) if p1.y <= p2.y else (p2, p1)
            return Segment(Dir.VERTICAL, start, end)
        elif p1.y == p2.y:
            (start, end) = (p1, p2) if p1.x <= p2.x else (p2, p1)
            return Segment(Dir.HORIZONTAL, start, end)
        else:
            return None

    def intersection(self, other) -> list[Point]:
        if self.dir == Dir.HORIZONTAL:
            y = self.start.y
            if other.dir == Dir.HORIZONTAL:
                if other.start.y == y:
                    start = max(self.start.x, other.start.x)
                    end = min(self.end.x, other.end.x)
                    return [Point(x, y) for x in range(start, end + 1)]
                else:
                    return []
            else:
                x = other.start.x
                intersect = \
                    self.start.x <= x <= self.end.x and other.start.y <= y <= other.end.y
                return [Point(x, y)] if intersect else []
        else:
            x = self.start.x
            if other.dir == Dir.VERTICAL:
                if other.start.x == x:
                    start = max(self.start.y, other.start.y)
                    end = min(self.end.y, other.end.y)
                    return [Point(x, y) for y in range(start, end + 1)]
                else:
                    return []
            else:
                y = other.start.y
                intersect = \
                    other.start.x <= x <= other.end.x and self.start.y <= y <= self.end.y
                return [Point(x, y)] if intersect else []


def solve(reader: io.TextIOBase) -> int:
    segments = []
    for line in reader.readlines():
        segment = Segment.parse(line)
        if segment is not None:
            segments.append(segment)

    intersections = set()
    for (i, segment1) in enumerate(segments):
        for j in range(i + 1, len(segments)):
            segment2 = segments[j]
            intersections.update(set(segment1.intersection(segment2)))
    return len(intersections)


assert solve(io.StringIO(EXAMPLE)) == 5


def main():
    with open("input/day05.txt") as file:
        result = solve(file)
        print(f"There are {result} points of overlap")


if __name__ == "__main__":
    main()
