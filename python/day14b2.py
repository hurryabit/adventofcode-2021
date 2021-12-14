from collections import Counter
from functools import cache
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


def solve(reader: io.TextIOBase) -> int:
    template = reader.readline().strip()
    reader.readline()
    rules = {line[:2]: line[6] for line in reader.readlines()}

    @cache
    def counts(pair: str, steps: int) -> Counter[str]:
        if steps == 0:
            return Counter()
        else:
            inner = rules[pair]
            return Counter({inner: 1}) \
                + counts(pair[0] + inner, steps - 1) \
                + counts(inner + pair[1], steps - 1)

    counter = sum(
        (counts(template[i:i+2], 40) for i in range(len(template) - 1)),
        start=Counter(template),
    )
    return max(counter.values()) - min(counter.values())


assert solve(io.StringIO(EXAMPLE)) == 2188189693529


def main():
    with open("input/day14.txt") as file:
        result = solve(file)
        print(f"The difference is {result}")


if __name__ == "__main__":
    main()
