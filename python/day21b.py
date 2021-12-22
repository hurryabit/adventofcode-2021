from functools import cache

ROLLS = [
    (3, 1),
    (4, 3),
    (5, 6),
    (6, 7),
    (7, 6),
    (8, 3),
    (9, 1),
]


def solve(player1: int, player2: int) -> int:
    @cache
    def go(pos1: int, pos2: int, score1: int, score2: int) -> tuple[int, int]:
        (wins1, wins2) = (0, 0)
        for (roll, freq) in ROLLS:
            pos1_next = (pos1 + roll - 1) % 10 + 1
            score1_next = score1 + pos1_next
            (sub_wins2, sub_wins1) = (0, 1) if score1_next >= 21 \
                else go(pos2, pos1_next, score2, score1_next)
            wins1 += freq * sub_wins1
            wins2 += freq * sub_wins2
        return (wins1, wins2)

    return max(go(player1, player2, 0, 0))


assert solve(4, 8) == 444356092776315


def main():
    with open("input/day20.txt") as file:
        result = solve(3, 10)
        print(f"The product is {result}")


if __name__ == "__main__":
    main()
