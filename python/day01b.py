from collections import deque


def main():
    with open("input/day01.txt") as file:
        result = 0
        window = deque()
        for line in file.readlines():
            window.append(int(line))
            if len(window) == 4:
                if window[-1] > window[0]:
                    result += 1
                window.popleft()
        print(f"{result} sums are larger")


if __name__ == "__main__":
    main()
