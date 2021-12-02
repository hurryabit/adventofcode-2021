import math


def main():
    with open("input/day02.txt") as file:
        (x_pos, y_pos, aim) = (0, 0, 0)
        for line in file.readlines():
            [cmd, arg] = line.split()
            arg = int(arg)
            if cmd == "forward":
                x_pos += arg
                y_pos += aim * arg
            elif cmd == "down":
                aim += arg
            elif cmd == "up":
                aim -= arg
            else:
                raise Exception("unknown command")
        print(f"The product of the final position is {x_pos * y_pos}")


if __name__ == "__main__":
    main()
