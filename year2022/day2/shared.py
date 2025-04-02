import enum
from typing import Any


class HandShape(enum.Enum):
    ROCK = ('A', 'X', 1)
    PAPER = ('B', 'Y', 2)
    SCISSORS = ('C', 'Z', 3)

    def __new__(cls, *values: Any):
        obj = object.__new__(cls)
        # First value is canonical value
        obj._value_ = values[0]
        # Second value can also be used for creation of enums
        cls._value2member_map_[values[1]] = obj
        return obj
    
    def __init__(self, opponent: str, response: str, score: int):
        self.opponent = opponent
        self.response = response
        self.score = score
    
    def round_score(self, opponent: 'HandShape') -> int:
        if opponent is self:
            return self.score + 3
        if ((self is HandShape.ROCK and opponent is HandShape.SCISSORS)
            or (self is HandShape.PAPER and opponent is HandShape.ROCK)
            or (self is HandShape.SCISSORS and opponent is HandShape.PAPER)):
            return self.score + 6
        return self.score
    
    @classmethod
    def for_result(cls, opponent: 'HandShape', result: str) -> 'HandShape':
        if result == 'Y':
            return opponent
        if opponent is cls.ROCK:
            return cls.PAPER if result == 'Z' else cls.SCISSORS
        if opponent is cls.SCISSORS:
            return cls.ROCK if result == 'Z' else cls.PAPER
        return cls.SCISSORS if result == 'Z' else cls.ROCK
