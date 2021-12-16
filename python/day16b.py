from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from math import prod


class limit(Iterator):
    items: Iterator
    count: int

    def __init__(self, items: Iterator, count: int):
        self.items = items
        self.count = count

    def exceeded(self) -> bool:
        return self.count <= 0

    def __next__(self):
        if not self.exceeded():
            self.count -= 1
            try:
                return next(self.items)
            except StopIteration:
                raise ValueError("iterator is too short")
        else:
            raise StopIteration


test_iter = iter(range(0, 6))
assert list(limit(test_iter, 3)) == [0, 1, 2]
assert list(test_iter) == [3, 4, 5]
try:
    list(limit(iter([0, 1]), 4))
    assert False
except ValueError:
    pass


def hex_bits(chars: str) -> Iterator[bool]:
    for char in chars:
        digit = int(char, base=16)
        for mask in [8, 4, 2, 1]:
            yield digit & mask != 0


assert list(hex_bits("8B")) == \
    [True, False, False, False, True, False, True, True]


def take_int(bits: Iterator[bool], width: int) -> int:
    result = 0
    for bit in limit(bits, width):
        result = result << 1
        if bit:
            result = result | 1
    return result


test_iter = iter([True, False, True, True, False])
assert take_int(test_iter, 3) == 5
assert list(test_iter) == [True, False]
try:
    take_int(iter([True, False]), 5)
    assert False
except ValueError:
    pass


@dataclass(frozen=True)
class Packet(ABC):
    version: int
    type: int

    def eval(self) -> int:
        raise NotImplementedError


@dataclass(frozen=True)
class Literal(Packet):
    value: int

    def eval(self) -> int:
        return self.value


@dataclass(frozen=True)
class Operator(Packet):
    operands: tuple[Packet]

    def eval(self) -> int:
        match self.type:
            case 0:
                return sum(operand.eval() for operand in self.operands)
            case 1:
                return prod(operand.eval() for operand in self.operands)
            case 2:
                return min(operand.eval() for operand in self.operands)
            case 3:
                return max(operand.eval() for operand in self.operands)
            case 5:
                (lhs, rhs) = self.operands
                return int(lhs.eval() > rhs.eval())
            case 6:
                (lhs, rhs) = self.operands
                return int(lhs.eval() < rhs.eval())
            case 7:
                (lhs, rhs) = self.operands
                return int(lhs.eval() == rhs.eval())
            case _:
                raise ValueError(f"invalid packet type: {self.type}")


literal = Literal(3, 4, 5)
assert literal.version == 3
assert literal.type == 4
assert literal.value == 5

operator = Operator(4, 3, [literal])
assert operator.version == 4
assert operator.type == 3
assert operator.operands == [literal]


TYPE_LITERAL = 4


def decode_int(bits: Iterator[bool]) -> int:
    result = 0
    more = True
    while more:
        more = next(bits)
        digit = take_int(bits, 4)
        result = result << 4 | digit
    return result


encode_0x8B = [True, True, False, False, False, False, True, False, True, True]
assert decode_int(iter(encode_0x8B)) == 0x8B


def decode_bits(bits: Iterator[bool]) -> Packet:
    version = take_int(bits, 3)
    type = take_int(bits, 3)
    if type == TYPE_LITERAL:
        value = decode_int(bits)
        return Literal(version=version, type=type, value=value)
    else:
        length_type = next(bits)
        if length_type:
            length = take_int(bits, 11)
            operands = [decode_bits(bits) for _ in range(length)]
        else:
            length = take_int(bits, 15)
            limited = limit(bits, length)
            operands = []
            while not limited.exceeded():
                operands.append(decode_bits(limited))
        return Operator(version=version, type=type, operands=tuple(operands))


def decode(chars: str) -> Packet:
    return decode_bits(hex_bits(chars))


assert decode("D2FE28") == Literal(version=6, type=4, value=2021)
assert decode("38006F45291200") == Operator(version=1, type=6, operands=(
    Literal(version=6, type=4, value=10),
    Literal(version=2, type=4, value=20),
))
assert decode("EE00D40C823060") == Operator(version=7, type=3, operands=(
    Literal(version=2, type=4, value=1),
    Literal(version=4, type=4, value=2),
    Literal(version=1, type=4, value=3),
))


def solve(chars: str) -> int:
    return decode(chars).eval()


assert solve("C200B40A82") == 3
assert solve("04005AC33890") == 54
assert solve("880086C3E88112") == 7
assert solve("CE00C43D881120") == 9
assert solve("D8005AC2A8F0") == 1
assert solve("F600BC2D8F") == 0
assert solve("9C005AC2F8F0") == 0
assert solve("9C0141080250320F1802104A08") == 1


def main():
    with open("input/day16.txt") as file:
        result = solve(file.read())
        print(f"The packet evaluates to {result}")


if __name__ == "__main__":
    main()
