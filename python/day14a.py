from collections import Counter
from itertools import chain
import io

EXAMPLE = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def step(polymer: str, rules: dict[str, str]) -> str:
    return "".join(chain(
        polymer[0],
        (
            rules[polymer[i - 1:i + 1]] + polymer[i]
            for i in range(1, len(polymer))
        )
    ))


def solve(reader: io.TextIOBase) -> int:
    template = reader.readline().strip()
    reader.readline()
    rules = {line[:2]: line[6] for line in reader.readlines()}

    polymer = template
    for _ in range(10):
        polymer = step(polymer, rules)

    counter = Counter(polymer)
    return max(counter.values()) - min(counter.values())


assert solve(io.StringIO(EXAMPLE)) == 1588


def main():
    with open("input/day14.txt") as file:
        result = solve(file)
        print(f"The difference is {result}")


if __name__ == "__main__":
    main()
