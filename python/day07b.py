from collections import deque

EXAMPLE = """16,1,2,0,4,2,7,1,2,14"""


def solve(input: str) -> int:
    def dist_fuel(dist):
        return dist * (dist + 1) // 2

    def fuel(position, submarines):
        return sum(dist_fuel(abs(submarine - position)) for submarine in submarines)

    submarines = list(map(int, input.split(",")))
    n = len(submarines)
    average = sum(submarines) // n
    min_fuel = fuel(average, submarines)
    offset = 0
    offset_fuel = min_fuel
    while offset_fuel <= min_fuel:
        offset += 1
        offset_fuel = min(
            fuel(average - offset, submarines),
            fuel(average + offset, submarines),
        )
        min_fuel = min(min_fuel, offset_fuel)

    return min_fuel


assert solve(EXAMPLE) == 168


def main():
    with open("input/day07.txt") as file:
        result = solve(file.read())
        print(f"The must spend {result} fuel")


if __name__ == "__main__":
    main()
