from collections import deque

EXAMPLE = """3,4,3,1,2"""


def solve(input: str) -> int:
    times = list(map(int, input.split(",")))
    fish_with_time = deque(9 * [0])
    for time in times:
        fish_with_time[time] += 1
    for _ in range(256):
        zeros = fish_with_time.popleft()
        fish_with_time[6] += zeros
        fish_with_time.append(zeros)
    return sum(fish_with_time)


assert solve(EXAMPLE) == 26984457539


def main():
    with open("input/day06.txt") as file:
        result = solve(file.read())
        print(f"There are {result} lanternfish")


if __name__ == "__main__":
    main()
