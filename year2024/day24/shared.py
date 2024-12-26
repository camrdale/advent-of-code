from collections.abc import Callable
from enum import Enum
import operator
from typing import NamedTuple


class Operation(Enum):
    AND = 1, operator.and_
    OR = 2, operator.or_
    XOR = 3, operator.xor

    def __init__(self, value: int, operator: Callable[[int, int], int]):
        super().__init__()
        self.operator = operator

    def apply(self, lhs: int, rhs: int) -> int:
        return self.operator(lhs, rhs)
    

class LogicEquation(NamedTuple):
    lhs: str
    operation: Operation
    rhs: str

    @classmethod
    def deterministic(cls, lhs: str, operation: Operation, rhs: str) -> 'LogicEquation':
        """Return a deterministic ordering of the equation."""
        # Sort because all operations don't care about lhs/rhs order.
        lhs, rhs = sorted((lhs, rhs))
        return cls(lhs, operation, rhs)

    def apply(self, known_bits: dict[str, int]) -> int:
        return self.operation.apply(known_bits[self.lhs], known_bits[self.rhs])
    
    def depends_on_all(self, equations: dict[str, 'LogicEquation']) -> set[str]:
        """Get all the wire results that this equation depends on."""
        dependencies: set[str] = set()
        dependencies.add(self.lhs)
        dependencies.add(self.rhs)
        if self.lhs in equations:
            dependencies.update(equations[self.lhs].depends_on_all(equations))
        if self.rhs in equations:
            dependencies.update(equations[self.rhs].depends_on_all(equations))
        return dependencies

    def depends_on_max_bit(
            self, 
            known_bits: dict[str, int], 
            equations: dict[str, 'LogicEquation']
            ) -> int:
        """Find the maximum bit number of any input wire that this equation depends on."""
        if self.lhs in known_bits:
            lhs_max_bit = int(self.lhs[1:])
        else:
            lhs_max_bit = equations[self.lhs].depends_on_max_bit(known_bits, equations)
        if self.rhs in known_bits:
            rhs_max_bit = int(self.rhs[1:])
        else:
            rhs_max_bit = equations[self.rhs].depends_on_max_bit(known_bits, equations)
        return max(lhs_max_bit, rhs_max_bit)

    def depends_on_equations(self, equations: dict[str, 'LogicEquation']) -> set['LogicEquation']:
        """Get all the equations that this equation depends on, including itself."""
        dependencies: set[LogicEquation] = set([self])
        if self.lhs in equations:
            dependencies.update(equations[self.lhs].depends_on_equations(equations))
        if self.rhs in equations:
            dependencies.update(equations[self.rhs].depends_on_equations(equations))
        return dependencies
    
    def __repr__(self) -> str:
        return self.lhs + ' ' + self.operation.name + ' ' + self.rhs


def to_num(num: str, known_bits: dict[str, int]) -> int:
    bitstring: list[str] = ['0']*64
    for bit, value in known_bits.items():
        if bit[0] == num:
            bit_num = int(bit[1:])
            bitstring[-1 - bit_num] = str(value)
    return int(''.join(bitstring), 2)


def calculate_z(
        known_bits: dict[str, int], 
        equations: dict[str, LogicEquation], 
        num_bits: int | None = None
        ) -> int:
    need_to_know: set[str] = set(
        bit for bit in equations
        if bit[0] =='z' and (num_bits is None or int(bit[1:]) < num_bits) and bit not in known_bits)

    while len(need_to_know) > 0:
        for bit in list(need_to_know):
            equation = equations[bit]
            if equation.lhs in known_bits and equation.rhs in known_bits:
                known_bits[bit] = equation.apply(known_bits)
                need_to_know.remove(bit)
            else:
                if equation.lhs not in known_bits:
                    need_to_know.add(equation.lhs)
                if equation.rhs not in known_bits:
                    need_to_know.add(equation.rhs)

    return to_num('z', known_bits)
