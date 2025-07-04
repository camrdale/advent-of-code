import collections
import re
from typing import NamedTuple, Self


ROOM_LIST = re.compile(r'([a-z-]*)-([0-9]*)\[([a-z]*)\]')


class RoomInfo(NamedTuple):
    encrypted_name: str
    sector_id: int
    expected_checksum: str

    @classmethod
    def from_text(cls, text: str) -> Self:
        match = ROOM_LIST.match(text)
        assert match is not None, text
        return cls(match.group(1), int(match.group(2)), match.group(3))
    
    def checksum(self) -> str:
        letters: collections.Counter[str] = collections.Counter(self.encrypted_name.replace('-', ''))

        # Negate the counts so the sort puts more common letters first,
        # but then sorts tied letters alphabetically.
        sorted_counts = sorted([
            (-count, letter) for letter, count in letters.most_common()])

        return ''.join(letter for _, letter in sorted_counts[:5])

    def checksum_passes(self) -> bool:
        return self.checksum() == self.expected_checksum

    def decrypt_name(self) -> str:
        room_name = ''
        for letter in self.encrypted_name:
            if letter == '-':
                room_name += ' '
                continue

            i = ord(letter) - ord('a')
            i = (i + self.sector_id) % 26
            room_name += chr(ord('a') + i)

        return room_name
