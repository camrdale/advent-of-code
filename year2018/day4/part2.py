from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2018.day4.shared import track_guards


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()
        input.sort()

        guards = track_guards(input)

        num_minutes, minute, guard = sorted([
            sleeps.most_common(1)[0][::-1] + (id,)
            for id, sleeps in guards.items()
            ], reverse=True)[0]

        log.log(log.RESULT, f'Guard {guard} sleeps {num_minutes} times during minute {minute}: {guard * minute}')
        return guard * minute


part = Part2()

part.add_result(4455, """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""")

part.add_result(10491)
