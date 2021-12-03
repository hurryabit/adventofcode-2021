import io

EXAMPLE_INPUT = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def digits_to_int(digits, base=10):
    result = 0
    for digit in digits:
        result = base * result + digit
    return result


def solve(reader):
    first = reader.readline()
    reader.seek(0)
    size = len(first.strip())
    counts = size * [0]
    total = 0
    for line in reader.readlines():
        total += 1
        for (i, digit) in enumerate(line.strip()):
            if digit == "1":
                counts[i] += 1
    gamma_digits = [int(2 * count >= total) for count in counts]
    gamma = digits_to_int(gamma_digits, base=2)
    epsilon = (1 << size) - 1 - gamma
    return gamma * epsilon


assert solve(io.StringIO(EXAMPLE_INPUT)) == 198


def main():
    with open("../input/day03.txt") as file:
        solution = solve(file)
        print(f"The power consumption of the submarine is {solution}")


if __name__ == "__main__":
    main()
