from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day7.shared import parse_directory_tree


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        root = parse_directory_tree(input)

        sum_of_small_directories = 0
        to_check = list(root.directories.values())
        while to_check:
            directory = to_check.pop()
            if directory.size() <= 100000:
                sum_of_small_directories += directory.size()
                log.log(log.INFO, f'Directory {directory.path()} has size <= 100000: {directory.size()}')
            to_check.extend(directory.directories.values())

        log.log(log.RESULT, f'The sum of sizes of all the directories of at most 100000: {sum_of_small_directories}')
        return sum_of_small_directories


part = Part1()

part.add_result(95437, r"""
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""")

part.add_result(1444896)
