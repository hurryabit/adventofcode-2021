import io
from typing import Optional

EXAMPLE = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def completion_score(line: str) -> Optional[int]:
    stack = []
    for char in line:
        if char in PAIRS:
            stack.append(PAIRS[char])
        elif len(stack) > 0 and stack[-1] == char:
            stack.pop()
        else:
            return None
    score = 0
    for char in reversed(stack):
        score = 5 * score + SCORES[char]
    return score


def solve(reader: io.TextIOBase) -> int:
    scores = []
    for line in reader.readlines():
        score = completion_score(line.strip())
        if score is not None:
            scores.append(score)
    scores.sort()
    return scores[len(scores) // 2]


assert solve(io.StringIO(EXAMPLE)) == 288957


def main():
    with open("input/day10.txt") as file:
        result = solve(file)
        print(f"The middle score is {result}")


if __name__ == "__main__":
    main()
