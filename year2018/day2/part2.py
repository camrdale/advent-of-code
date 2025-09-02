from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


def all_one_letter_replaced_possibilities(box_id: str) -> set[str]:
    return set(box_id[:i] + '0' + box_id[i+1:] for i in range(len(box_id)))


class Part2(Part):
    def run(self, parser: InputParser) -> str:
        input = parser.get_input()

        one_letter_replaced = all_one_letter_replaced_possibilities(input[0])
        for box_id in input[1:]:
            box_id_one_letter_replaced = all_one_letter_replaced_possibilities(box_id)
            common_box_ids = box_id_one_letter_replaced & one_letter_replaced
            if common_box_ids:
                assert len(common_box_ids) == 1, common_box_ids
                box_id = next(iter(common_box_ids))
                i = box_id.index('0')
                box_id = box_id[:i] + box_id[i+1:]
                log.log(log.RESULT, f'The common letters in the correct box ID: {box_id}')
                return box_id
            one_letter_replaced.update(box_id_one_letter_replaced)

        raise ValueError(f'Failed to find common box IDs: {one_letter_replaced}')


part = Part2()

part.add_result('fgij', """
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
""")

part.add_result('aixwcbzrmdvpsjfgllthdyoqe')
