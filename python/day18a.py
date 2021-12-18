from ast import literal_eval
from dataclasses import dataclass
import io
from typing import Any

EXAMPLE1 = """[1,1]
[2,2]
[3,3]
[4,4]"""
RESULT1 = [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]

EXAMPLE2 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""
RESULT2 = [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]

EXAMPLE3 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""
RESULT3 = [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]

EXAMPLE4 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
RESULT4 = [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]

EXAMPLE5 = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
RESULT5 = [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]],
           [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]


@dataclass
class Cell:
    data: list
    index: int

    def get(self):
        return self.data[self.index]

    def set(self, value):
        self.data[self.index] = value

    def add(self, value):
        self.set(self.get() + value)

    def is_int(self):
        return isinstance(self.get(), int)

    def left(self):
        return Cell(self.get(), 0)

    def right(self):
        return Cell(self.get(), 1)

    def left_most(self):
        cell = self
        while not cell.is_int():
            cell = cell.left()
        return cell

    def right_most(self):
        cell = self
        while not cell.is_int():
            cell = cell.right()
        return cell


Number = list[Any]


def explode(number: Number) -> bool:
    def go(cell: Cell, depth: int, left: Cell | None, right: Cell | None) -> bool:
        if cell.is_int():
            return False
        elif depth < 4:
            return go(cell.left(), depth + 1, left, cell.right()) \
                or go(cell.right(), depth + 1, cell.left(), right)
        else:
            [a, b] = cell.get()
            cell.set(0)
            if left is not None:
                left.right_most().add(a)
            if right is not None:
                right.left_most().add(b)
            return True

    return go(Cell([number], 0), 0, None, None)


def test_explode(before: Number, after: Number):
    assert explode(before) and before == after


test_explode([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4])
test_explode([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]])
test_explode([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3])
test_explode(
    [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]],
    [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
)
test_explode(
    [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
    [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
)


def split(number: Number) -> bool:
    def go(cell: Cell) -> bool:
        if cell.is_int():
            value = cell.get()
            if value >= 10:
                cell.set([value // 2, (value + 1) // 2])
                return True
            else:
                return False
        else:
            return go(cell.left()) or go(cell.right())

    return go(Cell([number], 0))


def normalize(number: Number) -> None:
    while explode(number) or split(number):
        pass


def add(lhs: Number, rhs: Number) -> Number:
    res = [lhs, rhs]
    normalize(res)
    return res


assert add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]) == \
    [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]


def add_file(reader: io.TextIOBase) -> Number:
    result = literal_eval(reader.readline())
    for line in reader.readlines():
        result = add(result, literal_eval(line))
    return result


assert add_file(io.StringIO(EXAMPLE1)) == RESULT1
assert add_file(io.StringIO(EXAMPLE2)) == RESULT2
assert add_file(io.StringIO(EXAMPLE3)) == RESULT3
assert add_file(io.StringIO(EXAMPLE4)) == RESULT4
assert add_file(io.StringIO(EXAMPLE5)) == RESULT5


def magnitude(number: Number) -> int:
    if isinstance(number, int):
        return number
    else:
        [left, right] = number
        return 3 * magnitude(left) + 2 * magnitude(right)


assert magnitude([[1, 2], [[3, 4], 5]]) == 143
assert magnitude([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == 1384
assert magnitude([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]) == 445
assert magnitude([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]) == 791
assert magnitude([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]) == 1137
assert magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]) == \
    3488


def solve(reader: io.TextIOBase) -> int:
    return magnitude(add_file(reader))


assert solve(io.StringIO(EXAMPLE5)) == 4140


def main():
    with open("input/day18.txt") as file:
        result = solve(file)
        print(f"The magnitude of the final sum is {result}")


if __name__ == "__main__":
    main()
