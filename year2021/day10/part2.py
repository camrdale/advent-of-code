from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

OPENING = {'(', '[', '{', '<'}
CLOSING_MAP = {')': '(', ']': '[', '}': '{', '>': '<'}
CLOSING_ERROR_SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}
COMPLETION_SCORES = {'(': 1, '[': 2, '{': 3, '<': 4}


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        autocompletion_scores: list[int] = []

        for line in input:
            pending_opens: list[str] = []
            for c in line:
                if c in OPENING:
                    pending_opens.append(c)
                    continue
                if not pending_opens or CLOSING_MAP[c] != pending_opens[-1]:
                    break
                pending_opens.pop()
            else:
                # No break, so no errors found.
                pending_opens.reverse()
                score = 0
                for c in pending_opens:
                    score *= 5
                    score += COMPLETION_SCORES[c]
                autocompletion_scores.append(score)

        autocompletion_scores.sort()
        middle_autocompletion_score = autocompletion_scores[int(len(autocompletion_scores) / 2)]
        log(RESULT, 'middle autocompletion score is:', middle_autocompletion_score)
        return middle_autocompletion_score


part = Part2()

part.add_result(288957, """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""")

part.add_result(4038824534)
