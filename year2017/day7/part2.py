import collections

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2017.day7.shared import Program


def find_imbalance(tower: Program) -> tuple[Program, int] | None:
    """Finds the imbalance in the tower.
    
    Returns None if the tower is balanced, otherwise the Program that
    needs to change and the weight it needs to change by.
    """
    match len(tower.supported):
        case 0:
            # Tower with no supported is always balanced
            return None
        case 1:
            raise ValueError(f'Tower {tower.name} has only one supported: {tower.supported}')
        case 2:
            # For towers of 2, can't know which is imbalanced, so check both
            tower1_imbalance = find_imbalance(tower.supported[0])
            tower2_imbalance = find_imbalance(tower.supported[0])
            if tower1_imbalance is not None:
                if tower2_imbalance is not None:
                    raise ValueError(f'Both towers cannot be imbalanced: {tower1_imbalance}, {tower2_imbalance}')
                return tower1_imbalance
            return tower2_imbalance
        case _:
            # With 3 or more towers, the imbalance is the one with a different total weight
            supported_weights = collections.Counter(
                supported.tower_weight for supported in tower.supported)
            if len(supported_weights) == 1:
                # No imbalance found
                return None
            if len(supported_weights) != 2 or supported_weights.most_common(2)[1][1] != 1:
                raise ValueError(f'Expected only one weight not to match: {supported_weights}')
            target_weight = supported_weights.most_common(1)[0][0]
            supported = [
                supported
                for supported in tower.supported
                if supported.tower_weight != target_weight][0]
            supported_imbalance = find_imbalance(supported)
            if supported_imbalance is not None:
                # Found the imbalance further up the tower
                if supported_imbalance[1] != target_weight - supported.tower_weight:
                    raise ValueError(
                        f'Expected the found imbalance to match the weight change needed: ' + 
                        f'{supported_imbalance[1]} != {target_weight} - {supported.tower_weight}')
                return supported_imbalance
            # Imbalance must be in the weight of this supported tower's base
            return supported, target_weight - supported.tower_weight


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        tower = Program.create_tower(input)

        imbalance = find_imbalance(tower)
        assert imbalance is not None

        log.log(log.RESULT, f'The program {imbalance[0].name} needs to have weight: {imbalance[0].weight + imbalance[1]}')
        return imbalance[0].weight + imbalance[1]


part = Part1()

part.add_result(60, """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
""")

part.add_result(802)
