import heapq
import io
import math

EXAMPLE = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


Matrix = list[list[int]]
Node = tuple[int, int]
Graph = dict[Node, list[tuple[Node, int]]]


def build_graph(matrix: Matrix) -> Graph:
    m = len(matrix)
    n = len(matrix[0])
    graph = {}
    for i0 in range(m):
        for j0 in range(n):
            edges = []
            for (di, dj) in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                (i1, j1) = (i0 + di, j0 + dj)
                if 0 <= i1 < m and 0 <= j1 < n:
                    edges.append(((i1, j1), matrix[i1][j1]))
            graph[(i0, j0)] = edges
    return graph


def dijkstra(graph: Graph, source: Node, target: Node) -> int:
    min_dists = {node: math.inf for node in graph}
    min_dists[source] = 0
    queue = [(0, source)]

    while len(queue) > 0:
        (node_dist, node) = heapq.heappop(queue)
        if node_dist > min_dists[node]:
            continue
        if node == target:
            return node_dist
        for (neighbor, edge_length) in graph[node]:
            neighbor_dist = node_dist + edge_length
            if neighbor_dist < min_dists[neighbor]:
                min_dists[neighbor] = neighbor_dist
                heapq.heappush(queue, (neighbor_dist, neighbor))

    return math.inf


def solve(reader: io.TextIOBase) -> int:
    matrix = [[int(d) for d in line.strip()] for line in reader.readlines()]
    m = len(matrix)
    n = len(matrix[0])
    M = 5 * m
    N = 5 * n

    def f(I, J):
        (k, i) = divmod(I, m)
        (l, j) = divmod(J, n)
        return (matrix[i][j] + k + l - 1) % 9 + 1

    MATRIX = [[f(I, J) for J in range(N)] for I in range(M)]
    graph = build_graph(MATRIX)
    return dijkstra(graph, (0, 0), (M - 1, N - 1))


assert solve(io.StringIO(EXAMPLE)) == 315


def main():
    with open("input/day15.txt") as file:
        result = solve(file)
        print(f"The lowest total risk is {result}")


if __name__ == "__main__":
    main()
