from enum import Enum
from functools import reduce
import math


LIMIT = 200


class Exp:
    def __init__(self, min=-math.inf, max=math.inf):
        assert min <= max
        self.min = min
        self.max = max

    def pretty(self, depth):
        return f"{depth * '  '}{self}"

    def simplify(self):
        match self:
            # Constant folding
            case Bin(op, Num(a), Num(b)): return Num(op.apply(a, b))

            # Constant folding with reassociation
            case Bin(Op.ADD, Bin(Op.ADD, a, Num(b)), Num(c)):
                return Bin(Op.ADD, a, Num(b + c)).simplify()

            # Neutral and absorbing elements
            case Bin(Op.ADD, a, Num(0)) | Bin(Op.ADD, Num(0), a): return a
            case Bin(Op.MUL, a, Num(1)) | Bin(Op.MUL, Num(1), a): return a
            case Bin(Op.DIV, a, Num(1)): return a
            case Bin(Op.MUL, _, Num(0)) | Bin(Op.MUL, Num(0), _): return Num(0)

            # Div/Mod range
            case Bin(Op.DIV, a, b) if 0 <= a.min and a.max < b.min: return Num(0)
            case Bin(Op.MOD, a, b) if 0 <= a.min and a.max < b.min: return a

            # Div/Mod distributivity
            case Bin(Op.DIV, Bin(Op.ADD, Bin(Op.MUL, a, b), c), d) if b is d:
                return Bin(Op.ADD, a, Bin(Op.DIV, c, d).simplify()).simplify()
            case Bin(Op.MOD, Bin(Op.ADD, Bin(Op.MUL, _, a), b), c) if a is c:
                return Bin(Op.MOD, b, c).simplify()

            # IfE case elimination
            case IfE(a, b, c, _) if a is b: return c
            case IfE(a, b, _, c) if a.max < b.min or a.min > b.max: return c

            # IfE distribution
            case Bin(op, IfE(a, b, c, d), e): return IfE(
                a,
                b,
                Bin(op, c, e.push_eql(a, b)).simplify(),
                Bin(op, d, e.push_neq(a, b)).simplify(),
            ).simplify()
            case Bin(op, a, IfE(b, c, d, e)): return IfE(
                b,
                c,
                Bin(op, a.push_eql(b, c), d).simplify(),
                Bin(op, a.push_neq(b, c), e).simplify(),
            ).simplify()

            # IfE hoisting
            case IfE(IfE(a, b, c, d), e, f, g): return IfE(
                a,
                b,
                IfE(c, e, f.push_eql(a, b), g.push_eql(a, b)).simplify(),
                IfE(d, e, f.push_neq(a, b), g.push_neq(a, b)).simplify(),
            ).simplify()

            case _: return self

    def push_eql(self, lhs, rhs):
        match self:
            case IfE(a, b, c, d):
                return c if a is lhs and b is rhs \
                    else IfE(a, b, c.push_eql(lhs, rhs), d.push_eql(lhs, rhs))
            case _: return self

    def push_neq(self, lhs, rhs):
        match self:
            case IfE(a, b, c, d):
                return d if a is lhs and b is rhs \
                    else IfE(a, b, c.push_neq(lhs, rhs), d.push_neq(lhs, rhs))
            case _: return self


class Inp(Exp):
    count = 0

    __match_args__ = ("index",)

    def __init__(self):
        super().__init__(min=1, max=9)
        self.index = Inp.count
        Inp.count += 1

    def __str__(self):
        return f"i{self.index}"


class Num(Exp):
    instances = {}

    __match_args__ = ("value",)

    def __new__(cls, value):
        if value in Num.instances:
            return Num.instances[value]
        else:
            return super().__new__(cls)

    def __init__(self, value):
        if value not in Num.instances:
            super().__init__(min=value, max=value)
            self.value = value
            Num.instances[value] = self

    def __str__(self):
        return str(self.value)


assert Num(0) is Num(0)
assert len(Num.instances) == 1 and Num.instances[0] is Num(0)


class Op(Enum):
    ADD = 0
    MUL = 1
    DIV = 2
    MOD = 3

    def symbol(self):
        match self:
            case self.ADD: return "+"
            case self.MUL: return "*"
            case self.DIV: return "/"
            case self.MOD: return "%"

    def min_max(self, lhs, rhs):
        match self:
            case self.ADD: return (lhs.min + rhs.min, lhs.max + rhs.max)
            case self.MUL:
                if lhs.min >= 0 and rhs.min >= 0:
                    return (lhs.min * rhs.min, lhs.max * rhs.max)
                else:
                    return (-math.inf, math.inf)
            case self.DIV: return (-math.inf, math.inf)
            case self.MOD: return (-math.inf, math.inf)

    def apply(self, lhs, rhs):
        match self:
            case self.ADD: return lhs + rhs
            case self.MUL: return lhs * rhs
            case self.DIV: return math.trunc(lhs / rhs)
            case self.MOD: return lhs % rhs


class Bin(Exp):
    __match_args__ = ("op", "lhs", "rhs")

    def __init__(self, op, lhs, rhs):
        (min, max) = op.min_max(lhs, rhs)
        super().__init__(min=min, max=max)
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f"({self.lhs} {self.op.symbol()} {self.rhs})"


class IfE(Exp):
    __match_args__ = ("lhs", "rhs", "then", "elze")

    def __init__(self, lhs, rhs, then, elze):
        super().__init__(min=min(then.min, elze.min), max=max(then.max, elze.max))
        self.lhs = lhs
        self.rhs = rhs
        self.then = then
        self.elze = elze

    def pretty(self, depth):
        return f"{depth * '  '}({self.lhs} = {self.rhs} ?\n{self.then.pretty(depth + 1)} :\n{self.elze.pretty(depth + 1)}\n{depth * '  '})"

    def __str__(self):
        return self.pretty(0)


class Constraint:
    pass


class Equal(Constraint):
    __match_args__ = ("lhs", "rhs")

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f"{self.lhs} = {self.rhs}"


class NotEq(Constraint):
    __match_args__ = ("lhs", "rhs")

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f"{self.lhs} <> {self.rhs}"


def clauses(exp):
    match exp:
        case IfE(lhs, rhs, then, elze):
            equal = Equal(lhs, rhs)
            for clause in clauses(then):
                yield [equal] + clause
            noteq = NotEq(lhs, rhs)
            for clause in clauses(elze):
                yield [noteq] + clause
        case _:
            if exp.min <= 0:
                if exp is Num(0):
                    yield []
                else:
                    yield [Equal(exp, Num(0))]


class Machine:
    def __init__(self):
        self.registers = {name: Num(0) for name in "wxyz"}

    def run(self, line):
        [cmd, *args] = line.split()
        if cmd == "inp":
            assert len(args) == 1
            [reg] = args
            assert reg in self.registers
            self.registers[reg] = Inp()
        else:
            assert len(args) == 2
            [reg, val] = args
            assert reg in self.registers
            lhs = self.registers[reg]
            rhs = self.registers[val] if val in self.registers \
                else Num(int(val))
            exp = IfE(lhs, rhs, Num(1), Num(0)) if cmd == "eql" \
                else Bin(Op[cmd.upper()], lhs, rhs)
            self.registers[reg] = exp.simplify()


def main():
    machine = Machine()
    with open("input/day24.txt") as file:
        for line in file.readlines():
            machine.run(line.strip())
    exp = machine.registers["z"]
    [clause] = list(clauses(exp))
    digits_a = 14 * [9]
    digits_b = 14 * [1]
    for constraint in clause:
        match constraint:
            case Equal(Bin(Op.ADD, Inp(i), Num(n)), Inp(j)):
                if n >= 0:
                    digits_a[i] = 9 - n
                    digits_b[j] = 1 + n
                else:
                    digits_a[j] = 9 + n
                    digits_b[i] = 1 - n
            case Equal(Inp(i), Inp(j)):
                pass
            case _: assert False
    result_a = reduce(lambda a, b: 10 * a + b, digits_a, 0)
    result_b = reduce(lambda a, b: 10 * a + b, digits_b, 0)
    print(f"The biggest model number is {result_a}")
    print(f"The smallest model number is {result_b}")


if __name__ == "__main__":
    main()
