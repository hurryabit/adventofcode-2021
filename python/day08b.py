from functools import reduce
import io
from typing import Callable

EXAMPLE = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def normalize(s: str) -> str:
    return "".join(sorted(s))


def deduce_table(digits: list[str]) -> list[str]:
    def is_subset(s: str, t: str) -> bool:
        return set(s) <= set(t)

    def find(pred: Callable[[str], bool]) -> str:
        return next(digit for digit in digits if pred(digit))

    result = 10 * [""]
    result[1] = find(lambda d: len(d) == 2)
    result[4] = find(lambda d: len(d) == 4)
    result[7] = find(lambda d: len(d) == 3)
    result[8] = find(lambda d: len(d) == 7)
    result[9] = find(lambda d: len(d) == 6 and is_subset(result[4], d))
    result[0] = find(
        lambda d: len(d) == 6 and is_subset(result[1], d) and d != result[9])
    result[6] = find(lambda d: len(d) == 6 and d not in {result[0], result[9]})
    result[3] = find(lambda d: len(d) == 5 and is_subset(result[1], d))
    result[5] = find(lambda d: len(d) == 5 and is_subset(d, result[6]))
    result[2] = find(lambda d: len(d) == 5 and d not in {result[3], result[5]})

    return result


def parse(digits: list[str], table: list[str]) -> int:
    return reduce(lambda n, d: 10 * n + table.index(d), digits, 0)


def solve(reader: io.TextIOBase) -> int:
    result = 0
    for line in reader.readlines():
        words = list(map(normalize, line.strip().split()))
        table = deduce_table(words[:10])
        result += parse(words[11:], table)
    return result


assert solve(io.StringIO(EXAMPLE)) == 61229


def main():
    with open("input/day08.txt") as file:
        result = solve(file)
        print(f"The output values add up to {result}")


if __name__ == "__main__":
    main()
