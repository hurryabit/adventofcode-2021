import math


def main():
    with open("input/day01.txt") as file:
        result = 0
        last = math.inf
        for line in file.readlines():
            current = int(line)
            if current > last:
                result += 1
            last = current
        print(f"{result} measurements are larger")


if __name__ == "__main__":
    main()
