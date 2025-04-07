from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2022.day7.shared import parse_directory_tree


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        root = parse_directory_tree(input)

        used_space = root.size()
        unused_space = 70000000 - used_space
        need_to_delete = 30000000 - unused_space
        log.log(log.INFO, f'Total used space is {used_space}, leaving {unused_space} unused, need to delete at least {need_to_delete}')
        assert need_to_delete > 0

        smallest_to_delete = root.size()
        to_check = list(root.directories.values())
        while to_check:
            directory = to_check.pop()
            if need_to_delete <= directory.size() < smallest_to_delete:
                smallest_to_delete = directory.size()
                log.log(log.INFO, f'Found new candidate directory for deletion with size {directory.size()}: {directory.path()}')
            to_check.extend(directory.directories.values())

        log.log(log.RESULT, f'The smallest directory to delete has size: {smallest_to_delete}')
        return smallest_to_delete


part = Part2()

part.add_result(24933642, r"""
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

part.add_result(404395)
