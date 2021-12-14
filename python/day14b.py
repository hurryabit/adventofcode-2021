from collections import Counter
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


class Polymer:
    def __init__(self, polymer):
        assert len(polymer) >= 3
        self.first = polymer[:2]
        self.inner = Counter()
        for i in range(1, len(polymer) - 2):
            self.inner[polymer[i:i + 2]] += 1
        self.last = polymer[-2:]

    def __str__(self):
        return f"Polymer(first={self.first}, inner={self.inner}, last={self.last})"

    def step(self, rules):
        (self.first, second) = rules[self.first]
        inner = Counter()
        inner[second] += 1
        for (pair, count) in self.inner.items():
            (pair1, pair2) = rules[pair]
            inner[pair1] += count
            inner[pair2] += count
        (penultimate, self.last) = rules[self.last]
        inner[penultimate] += 1
        self.inner = inner

    def counts(self):
        result = Counter(self.first)
        for (pair, count) in self.inner.items():
            result[pair[-1]] += count
        result[self.last[-1]] += 1
        return result


def solve(reader: io.TextIOBase) -> int:
    template = reader.readline().strip()
    reader.readline()
    rules = {
        line[:2]: (line[0] + line[6], line[6] + line[1])
        for line in reader.readlines()
    }

    polymer = Polymer(template)
    for _ in range(40):
        polymer.step(rules)

    counter = polymer.counts()
    return max(counter.values()) - min(counter.values())


assert solve(io.StringIO(EXAMPLE)) == 2188189693529


def main():
    with open("input/day14.txt") as file:
        result = solve(file)
        print(f"The difference is {result}")


if __name__ == "__main__":
    main()
