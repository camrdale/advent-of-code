from typing import NamedTuple

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from year2023.day15.shared import hash_function


class Lens(NamedTuple):
    label: str
    focal_length: int

    def __str__(self) -> str:
        return f'[{self.label} {self.focal_length}]'


class Box:
    def __init__(self, number: int):
        self.number = number
        self.lenses: list[Lens] = []

    def __str__(self) -> str:
        return f'Box {self.number}: ' + ' '.join(str(lens) for lens in self.lenses)
    
    def is_empty(self) -> bool:
        return len(self.lenses) == 0
    
    def remove(self, label: str):
        for i, lens in enumerate(self.lenses):
            if lens.label == label:
                del self.lenses[i]
                return
            
    def insert(self, new_lens: Lens):
        for i, lens in enumerate(self.lenses):
            if lens.label == new_lens.label:
                self.lenses[i] = new_lens
                return
        self.lenses.append(new_lens)

    def focusing_power(self) -> int:
        power = 0
        for i, lens in enumerate(self.lenses):
            power += (self.number + 1) * (i + 1) * (lens.focal_length)
        return power


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        boxes: list[Box] = [Box(i) for i in range(256)]
        for step in input[0].split(','):
            if step.endswith('-'):
                label = step[:-1]
                box_number = hash_function(label)
                boxes[box_number].remove(label)
            else:
                label, focal_length = step.split('=')
                lens = Lens(label, int(focal_length))
                box_number = hash_function(label)
                boxes[box_number].insert(lens)
            log(INFO, f'After "{step}":\n' + '\n'.join(str(box) for box in boxes if not box.is_empty()) + '\n')

        focusing_power = 0
        for box in boxes:
            focusing_power += box.focusing_power()

        log(RESULT, f'The focusing power of the lenses: {focusing_power}')
        return focusing_power


part = Part2()

part.add_result(145, """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
""")

part.add_result(260530)
