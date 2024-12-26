from aoc.input import InputParser
from aoc.log import log, RESULT
from aoc.runner import Part

OPENING = {'(', '[', '{', '<'}
CLOSING_MAP = {')': '(', ']': '[', '}': '{', '>': '<'}
CLOSING_ERROR_SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}
COMPLETION_SCORES = {'(': 1, '[': 2, '{': 3, '<': 4}


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        syntax_score = 0

        for line in input:
            chunks = list(line)
            pending_opens: list[str] = []
            for c in chunks:
                if c in OPENING:
                    pending_opens.append(c)
                    continue
                if not pending_opens or CLOSING_MAP[c] != pending_opens[-1]:
                    syntax_score += CLOSING_ERROR_SCORES[c]
                    break
                pending_opens.pop()
            else:
                # No break, so no errors found.
                pending_opens.reverse()
                score = 0
                for c in pending_opens:
                    score *= 5
                    score += COMPLETION_SCORES[c]

        log(RESULT, 'total syntax error score is:', syntax_score)
        return syntax_score


part = Part1()

part.add_result(26397, """
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

part.add_result(268845)
