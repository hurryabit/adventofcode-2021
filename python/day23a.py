from dataclasses import dataclass, replace
from heapq import heappush, heappop
import math
from typing import Callable, ClassVar, Generator, Iterator


def dijkstra(
    source: str,
    neighbors: Callable[[str], Iterator[tuple[str, int]]],
    target: str,
) -> int:
    distances = {source: 0}
    queue = [(0, source)]

    while len(queue) > 0:
        (node_dist, node) = heappop(queue)
        if node_dist > distances[node]:
            continue
        if node == target:
            return node_dist

        for (neighbor, edge_dist) in neighbors(node):
            neighbor_dist = node_dist + edge_dist
            if neighbor not in distances or neighbor_dist < distances[neighbor]:
                distances[neighbor] = neighbor_dist
                heappush(queue, (neighbor_dist, neighbor))

    return math.inf


CAVE_DEPTH = 2
CAVE_COLS = {"A": 2, "B": 4, "C": 6, "D": 8}
COST = {"A": 1, "B": 10, "C": 100, "D": 1000}


@dataclass(frozen=True)
class Coord:
    row: int
    col: int

    ALL: ClassVar[list] = []

    def index(self) -> int:
        if self.row == 0:
            return self.col
        else:
            return 11 + (self.col - 1) // 2 * CAVE_DEPTH + self.row - 1

    def dist(self, other) -> int:
        return abs(self.row - other.row) + abs(self.col - other.col)

    def south(self) -> int:
        return replace(self, row=self.row + 1)

    def north(self) -> int:
        return replace(self, row=self.row - 1)

    def east(self) -> int:
        return replace(self, col=self.col + 1)

    def west(self) -> int:
        return replace(self, col=self.col - 1)

    def path_to(self, finish) -> Generator:
        current = self
        while current != finish:
            if current.col == finish.col:
                assert 0 <= current.row < finish.row
                current = current.south()
            elif current.row > 0:
                assert finish.row == 0 and finish.col != current.col
                current = current.north()
            elif current.col < finish.col:
                assert current.row == 0
                current = current.east()
            elif current.col > finish.col:
                assert current.row == 0
                current = current.west()
            else:
                assert False
            yield current


Coord.ALL = [Coord(0, col) for col in range(11)] + [
    Coord(row, col)
    for row in range(1, CAVE_DEPTH + 1)
    for col in CAVE_COLS.values()
]

assert len(Coord.ALL) == 11 + 4 * CAVE_DEPTH


assert Coord(0, 0).index() == 0
assert Coord(0, 10).index() == 10
assert Coord(1, 2).index() == 11
assert Coord(CAVE_DEPTH, 2).index() == 10 + CAVE_DEPTH
assert Coord(1, 8).index() == 11 + 3 * CAVE_DEPTH
assert Coord(CAVE_DEPTH, 8).index() == 10 + 4 * CAVE_DEPTH

assert list(Coord(0, 0).path_to(Coord(2, 2))) == \
    [Coord(0, 1), Coord(0, 2), Coord(1, 2), Coord(2, 2)]
assert list(Coord(2, 4).path_to(Coord(0, 7))) == \
    [Coord(1, 4), Coord(0, 4), Coord(0, 5), Coord(0, 6), Coord(0, 7)]


@dataclass(frozen=True, order=True)
class State:
    data: str

    FINISH: ClassVar

    def __post_init__(self):
        assert len(self.data) == 11 + 4 * CAVE_DEPTH

    @classmethod
    def make(cls, data: list[str]):
        return State("..x.x.x.x.." + "".join(data))

    def __getitem__(self, coord: Coord) -> str:
        return self.data[coord.index()]

    def move(self, start: Coord, finish: Coord):
        (i, j) = (start.index(), finish.index())
        if i > j:
            (i, j) = (j, i)
        assert i < j
        data = self.data
        data = data[:i] + data[j] + data[i+1:j] + data[i] + data[j+1:]
        return State(data)

    def path_clear(self, start: Coord, finish: Coord) -> bool:
        return all(self[coord] in ".x" for coord in start.path_to(finish))

    def moves(self) -> Generator:
        for start_col in CAVE_COLS.values():
            start = Coord(row=1, col=start_col)
            while start.row <= CAVE_DEPTH and self[start] == ".":
                start = start.south()
            if start.row <= CAVE_DEPTH:
                kind = self[start]
                if CAVE_COLS[kind] != start_col:
                    can_move = True
                else:
                    rest = start.south()
                    while rest.row <= CAVE_DEPTH and self[rest] == kind:
                        rest = rest.south()
                    can_move = rest.row <= CAVE_DEPTH
                if can_move:
                    for finish_col in range(11):
                        finish = Coord(row=0, col=finish_col)
                        if self[finish] == "." and self.path_clear(start, finish):
                            yield (self.move(start, finish), COST[kind] * start.dist(finish))

        for start_col in range(11):
            start = Coord(row=0, col=start_col)
            kind = self[start]
            if kind not in CAVE_COLS:
                continue
            finish_col = CAVE_COLS[kind]
            finish = Coord(row=1, col=finish_col)
            if not self.path_clear(start, finish):
                continue
            while finish.row < CAVE_DEPTH and self[finish.south()] == ".":
                finish = finish.south()
            rest = finish.south()
            while rest.row <= CAVE_DEPTH and self[rest] == kind:
                rest = rest.south()
            if rest.row <= CAVE_DEPTH:
                continue
            yield (self.move(start, finish), COST[kind] * start.dist(finish))


State.FINISH = State.make([CAVE_DEPTH * kind for kind in "ABCD"])

assert State.FINISH.data == "..x.x.x.x..AABBCCDD"

EXAMPLE = State.make(["BA", "CD", "BC", "DA"])

assert EXAMPLE.data == "..x.x.x.x..BACDBCDA"

assert EXAMPLE[Coord(0, 0)] == "."
assert EXAMPLE[Coord(0, 2)] == "x"
assert EXAMPLE[Coord(0, 10)] == "."
assert EXAMPLE[Coord(1, 2)] == "B"
assert EXAMPLE[Coord(CAVE_DEPTH, 2)] == "A"
assert EXAMPLE[Coord(1, 8)] == "D"
assert EXAMPLE[Coord(CAVE_DEPTH, 8)] == "A"

assert EXAMPLE.move(Coord(1, 2), Coord(0, 3)).data == "..xBx.x.x...ACDBCDA"
assert EXAMPLE.\
    move(Coord(1, 2), Coord(0, 3)).\
    move(Coord(1, 4), Coord(1, 2)).\
    move(Coord(0, 3), Coord(1, 3)) == State.make(["CA", "BD", "BC", "DA"])

assert EXAMPLE.path_clear(Coord(1, 2), Coord(0, 3))
assert EXAMPLE.\
    move(Coord(1, 2), Coord(0, 3)).\
    path_clear(Coord(0, 3), Coord(1, 2))
assert not EXAMPLE.\
    move(Coord(1, 2), Coord(0, 3)).\
    path_clear(Coord(1, 4), Coord(0, 1))
assert len(list(EXAMPLE.moves())) == 28
assert len(list(EXAMPLE.move(Coord(1, 2), Coord(0, 3)).moves())) == 12
assert len(list(EXAMPLE.move(Coord(1, 4), Coord(0, 3)).moves())) == 14

EXAMPLE2 = \
    EXAMPLE.move(Coord(1, 6), Coord(0, 7)).move(Coord(1, 4), Coord(0, 5))
assert (EXAMPLE2.move(Coord(0, 5), Coord(1, 6)), 200) in list(EXAMPLE2.moves())
EXAMPLE3 = \
    EXAMPLE.move(Coord(1, 4), Coord(0, 3)).move(Coord(1, 6), Coord(0, 5))
assert \
    (EXAMPLE3.move(Coord(0, 5), Coord(1, 4)), 20) not in list(EXAMPLE3.moves())


def solve(source: State) -> int:
    return dijkstra(
        source,
        lambda state: state.moves(),
        State.FINISH,
    )


assert solve(EXAMPLE) == 12521


def main():
    result = solve(State.make(["CB", "AA", "DB", "DC"]))
    print(f"The amphipods required {result} energy")


if __name__ == "__main__":
    main()
