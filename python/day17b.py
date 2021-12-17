from collections import defaultdict
from math import sqrt, floor, ceil


def solve(x_min: int, x_max: int, y_min: int, y_max: int) -> int:
    v_y_for_time = defaultdict(list)
    v_y_min = y_min
    v_y_max = -y_min - 1

    for v_y in range(v_y_min, v_y_max + 1):
        v = v_y
        y = 0
        t = 0
        while y >= y_min:
            y += v
            v -= 1
            t += 1
            if y_min <= y <= y_max:
                v_y_for_time[t].append(v_y)

    result = set()
    for (t, v_ys) in v_y_for_time.items():
        a = max(t, ceil(x_min / t + (t - 1) / 2))
        b = floor(x_max / t + (t - 1) / 2)
        for v_x in range(a, b + 1):
            for v_y in v_ys:
                result.add((v_x, v_y))

        a = ceil(sqrt(2 * x_min + 0.25) - 0.5)
        b = min(t - 1, floor(sqrt(2 * x_max + 0.25) - 0.5))
        for v_x in range(a, b + 1):
            for v_y in v_ys:
                result.add((v_x, v_y))

    return len(result)


assert solve(20, 30, -10, -5) == 112


def main():
    result = solve(257, 286, -101, -57)
    print(f"{result} distinct initial velocities work")


if __name__ == "__main__":
    main()
