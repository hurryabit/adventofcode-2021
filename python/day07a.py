from collections import deque

EXAMPLE = """16,1,2,0,4,2,7,1,2,14"""


def solve(input: str) -> int:
    submarines = list(map(int, input.split(",")))
    submarines.sort()
    n = len(submarines)
    median = submarines[n // 2]
    return sum(abs(submarine - median) for submarine in submarines)


assert solve(EXAMPLE) == 37


def main():
    with open("input/day07.txt") as file:
        result = solve(file.read())
        print(f"The must spend {result} fuel")


if __name__ == "__main__":
    main()
