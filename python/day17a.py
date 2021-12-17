from math import sqrt, floor, ceil


def solve(x_min: int, x_max: int, y_min: int, y_max: int) -> int:
    if ceil(sqrt(2 * x_min + 0.25) - 0.5) <= floor(sqrt(2 * x_max + 0.25) - 0.5):
        return (y_min + 1) * y_min // 2
    else:
        raise Exception("more complex solution required")


assert solve(20, 30, -10, -5) == 45


def main():
    result = solve(257, 286, -101, -57)
    print(f"The packet evaluates to {result}")


if __name__ == "__main__":
    main()
