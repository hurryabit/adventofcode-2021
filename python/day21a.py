def solve(player1: int, player2: int) -> int:
    next_roll = 1
    num_rolls = 0

    def roll() -> int:
        nonlocal next_roll
        nonlocal num_rolls
        result = next_roll
        next_roll = next_roll % 100 + 1
        num_rolls += 1
        return result

    locations = [player1, player2]
    scores = [0, 0]
    player = 0

    while scores[0] < 1000 and scores[1] < 1000:
        locations[player] = \
            (locations[player] + roll() + roll() + roll() - 1) % 10 + 1
        scores[player] += locations[player]
        player = 1 - player

    return num_rolls * scores[player]


assert solve(4, 8) == 739785


def main():
    with open("input/day20.txt") as file:
        result = solve(3, 10)
        print(f"The product is {result}")


if __name__ == "__main__":
    main()
