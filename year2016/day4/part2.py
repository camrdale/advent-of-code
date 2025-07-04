from aoc.input import InputParser
from aoc import log
from aoc.runner import Part

from year2016.day4.shared import RoomInfo


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        for line in input:
            room = RoomInfo.from_text(line)
            if not room.checksum_passes():
                continue

            room_name = room.decrypt_name()
            log.log(log.INFO, f'Decrypted room name for sector ID {room.sector_id}: {room_name}')

            if 'north' in room_name and 'pole' in room_name:
                log.log(log.RESULT, f'North Pole objects are stored in sector ID {room.sector_id}: {room_name}')
                return room.sector_id

        raise ValueError(f'Failed to find the room where North Pole objects are stored.')


part = Part2()

part.add_result(501)
