from collections import defaultdict
import io

EXAMPLE1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

EXAMPLE2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

EXAMPLE3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


Graph = dict[str, list[str]]


def dfs(graph: Graph, v: str, seen: frozenset[int], joker: bool):
    if v == "end":
        return 1
    if v in seen:
        if not joker or v == "start":
            return 0
        joker = False
    if v.islower():
        seen = seen | {v}
    return sum(dfs(graph, w, seen, joker) for w in graph[v])


def solve(reader: io.TextIOBase) -> int:
    graph: Graph = defaultdict(list)
    for line in reader.readlines():
        [u, v] = line.strip().split("-")
        graph[u].append(v)
        graph[v].append(u)

    return dfs(graph, "start", frozenset(), True)


assert solve(io.StringIO(EXAMPLE1)) == 36
assert solve(io.StringIO(EXAMPLE2)) == 103
assert solve(io.StringIO(EXAMPLE3)) == 3509


def main():
    with open("input/day12.txt") as file:
        result = solve(file)
        print(f"There are {result} paths")


if __name__ == "__main__":
    main()
