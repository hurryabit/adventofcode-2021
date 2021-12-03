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


def filter_step(numbers, index, keep_majority):
    count = len(numbers)
    count_ones = sum(1 for number in numbers if number[index] == "1")
    majority = 1 if 2 * count_ones >= count else 0
    minority = 1 - majority
    keep = str(majority if keep_majority else minority)
    return [number for number in numbers if number[index] == keep]


def filter(numbers, keep_majority):
    index = 0
    while len(numbers) > 1:
        numbers = filter_step(numbers, index, keep_majority)
        index += 1
    return digits_to_int([int(digit) for digit in numbers[0]], base=2)


def solve(reader):
    numbers = [line.strip() for line in reader.readlines()]
    oxygen_rating = filter(numbers, True)
    co2_rating = filter(numbers, False)
    return oxygen_rating * co2_rating


assert solve(io.StringIO(EXAMPLE_INPUT)) == 230


def main():
    with open("../input/day03.txt") as file:
        solution = solve(file)
        print(f"The life support rating of the submarine is {solution}")


if __name__ == "__main__":
    main()
