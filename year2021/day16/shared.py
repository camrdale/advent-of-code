import math
from typing import Self

from aoc import log


class Packet:
    def __init__(self, bits: str):
        log.log(log.DEBUG, f'Parsing packet from string: {bits}')
        self.version = int(bits[:3], 2)
        self.type = int(bits[3:6], 2)
        self.sub_packets: list[Packet] = []
        self.length = 6
        if self.type == 4:
            literal = ''
            while bits[self.length] == '1':
                literal += bits[self.length+1:self.length+5]
                self.length += 5
            literal += bits[self.length+1:self.length+5]
            self.length += 5
            self.literal = int(literal, 2)
        else:
            if bits[self.length] == '0':
                sub_packet_length = int(bits[self.length+1:self.length+16], 2)
                self.length += 16
                while sub_packet_length > 0:
                    sub_packet = Packet(bits[self.length:self.length+sub_packet_length])
                    sub_packet_length -= sub_packet.length
                    self.length += sub_packet.length
                    self.sub_packets.append(sub_packet)
            else:
                num_sub_packets = int(bits[self.length+1:self.length+12], 2)
                self.length += 12
                while num_sub_packets > 0:
                    sub_packet = Packet(bits[self.length:])
                    num_sub_packets -= 1
                    self.length += sub_packet.length
                    self.sub_packets.append(sub_packet)

    @classmethod
    def from_text(cls, text: str) -> Self:
        bits = ''.join(map(str, [1 if digit=='1' else 0 for c in text for digit in f'{int(c, 16):0>4b}']))
        return cls(bits)

    def sum_versions(self) -> int:
        return self.version + sum(packet.sum_versions() for packet in self.sub_packets)
    
    def value(self) -> int:
        match self.type:
            case 0:
                return sum(packet.value() for packet in self.sub_packets)
            case 1:
                return math.prod(packet.value() for packet in self.sub_packets)
            case 2:
                return min(packet.value() for packet in self.sub_packets)
            case 3:
                return max(packet.value() for packet in self.sub_packets)
            case 4:
                return self.literal
            case 5:
                return int(self.sub_packets[0].value() > self.sub_packets[1].value())
            case 6:
                return int(self.sub_packets[0].value() < self.sub_packets[1].value())
            case 7:
                return int(self.sub_packets[0].value() == self.sub_packets[1].value())
            case _:
                raise ValueError(f'Unexpected packet type: {self.type}')
