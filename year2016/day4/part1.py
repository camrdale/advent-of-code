from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day4.shared import RoomInfo


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        sector_ids = 0
        for line in input:
            room = RoomInfo.from_text(line)
            if room.checksum_passes():
                sector_ids += room.sector_id

        log.log(log.RESULT, f'The sum of the sector IDs of the real rooms: {sector_ids}')
        return sector_ids


part = Part1()

part.add_result(1514, """
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
""")

part.add_result(137896)
