import io

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
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def error_score(line: str) -> int:
    stack = []
    for char in line:
        if char in PAIRS:
            stack.append(PAIRS[char])
        elif len(stack) > 0 and stack[-1] == char:
            stack.pop()
        else:
            return SCORES[char]
    return 0


def solve(reader: io.TextIOBase) -> int:
    total_score = 0
    for line in reader.readlines():
        total_score += error_score(line.strip())
    return total_score


assert solve(io.StringIO(EXAMPLE)) == 26397


def main():
    with open("input/day10.txt") as file:
        result = solve(file)
        print(f"The total syntax error score is {result}")


if __name__ == "__main__":
    main()
