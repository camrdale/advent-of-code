from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2015.day13.shared import SeatingArranger


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        arranger = SeatingArranger(input)

        arranger.guests.add('Cameron')

        best_arrangement = arranger.optimal_arrangement()

        log.log(log.RESULT, f'The total change in happiness for the optimal seating arrangement: {best_arrangement}')
        return best_arrangement


part = Part2()

part.add_result(286, """
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
""")

part.add_result(668)
