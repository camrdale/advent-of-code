from abc import ABC, abstractmethod
import collections
import re

from aoc import log


INSTRUCTION = re.compile(r'bot ([0-9]*) gives low to (bot|output) ([0-9]*) and high to (bot|output) ([0-9]*)')
VALUE = re.compile(r'value ([0-9]*) goes to bot ([0-9]*)')


class ChipDestination(ABC):
    @abstractmethod
    def receive_value(self, value: int) -> bool:
        """Receive a value and return if a bot is ready to proceed with its values."""
        pass


class Bot(ChipDestination):
    def __init__(self) -> None:
        self.values: list[int] = []

    def initialize(self, num: int, low: ChipDestination, high: ChipDestination) -> None:
        self.num = num
        self.low = low
        self.high = high

    def receive_value(self, value: int) -> bool:
        assert len(self.values) < 2, f'Bot {self.num} received third value {value}: {self.values}'
        self.values.append(value)
        return len(self.values) == 2
    
    def proceed(self) -> list['Bot']:
        assert len(self.values) == 2, f'Bot {self.num} does not have 2 values: {self.values}'
        lower_value = min(self.values)
        upper_value = max(self.values)
        active: list[Bot] = []
        if self.low.receive_value(lower_value):
            assert isinstance(self.low, Bot)
            active.append(self.low)
        if self.high.receive_value(upper_value):
            assert isinstance(self.high, Bot)
            active.append(self.high)
        return active
    
    def check_condition(self, condition: tuple[int, int]) -> bool:
        assert len(self.values) == 2, f'Bot {self.num} does not have 2 values: {self.values}'
        return self.values[0] in condition and self.values[1] in condition


class Output(ChipDestination):
    def __init__(self) -> None:
        self.values: list[int] = []

    def receive_value(self, value: int) -> bool:
        self.values.append(value)
        return False


class BalanceBots:
    def __init__(self, instructions: list[str]) -> None:
        self.instructions = instructions
        self.bots: dict[int, Bot] = collections.defaultdict(Bot)
        self.outputs: dict[int, Output] = collections.defaultdict(Output)

        for instruction in instructions:
            match = INSTRUCTION.match(instruction)
            if not match:
                continue
            num = int(match.group(1))
            low_num = int(match.group(3))
            low = self.bots[low_num] if match.group(2) == 'bot' else self.outputs[low_num]
            high_num = int(match.group(5))
            high = self.bots[high_num] if match.group(4) == 'bot' else self.outputs[high_num]
            self.bots[num].initialize(num, low, high)
        
    def run(self, stop_condition: tuple[int, int] | None = None) -> int:
        active: list[Bot] = []
        for instruction in self.instructions:
            match = VALUE.match(instruction)
            if not match:
                continue
            value = int(match.group(1))
            bot_num = int(match.group(2))
            if self.bots[bot_num].receive_value(value):
                active.append(self.bots[bot_num])

        while active:
            newly_active: list[Bot] = []
            for bot in active:
                if stop_condition and bot.check_condition(stop_condition):
                    return bot.num
                newly_active.extend(bot.proceed())
                active = newly_active

        assert not stop_condition, f'Failed to find stop condition: {stop_condition}'
        for num, output in self.outputs.items():
            log.log(log.INFO, f'Output {num}: {output.values}')
        return self.outputs[0].values[0] * self.outputs[1].values[0] * self.outputs[2].values[0]
