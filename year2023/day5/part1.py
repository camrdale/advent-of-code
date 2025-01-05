from typing import NamedTuple, TypeVar, Generic, Any

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO, DEBUG
from aoc.runner import Part


class AlmanacType(NamedTuple):
    value: int


class Seed(AlmanacType):
    pass


class Soil(AlmanacType):
    pass


class Fertilizer(AlmanacType):
    pass


class Water(AlmanacType):
    pass


class Light(AlmanacType):
    pass


class Temperature(AlmanacType):
    pass


class Humidity(AlmanacType):
    pass


class Location(AlmanacType):
    pass


Source = TypeVar('Source', bound=AlmanacType)
Destination = TypeVar('Destination', bound=AlmanacType)


class AlmanacConverter(Generic[Source, Destination]):
    def __init__(
            self,
            line: str,
            destination_type: type[Destination]):
        self.destination_start, self.source_start, self.range_length = map(int, line.split())
        self.destination_type = destination_type

    def contains(self, source: Source) -> bool:
        return self.source_start <= source.value < self.source_start + self.range_length

    def convert(self, source: Source) -> Destination:
        return self.destination_type(source.value + self.destination_start - self.source_start)

    def __lt__(self, other: Any) -> bool:
        assert type(other) == AlmanacConverter
        return self.source_start < other.source_start
    
    def __str__(self) -> str:
        return f'AlmanacConverter[{self.destination_type.__name__}]({self.source_start}, {self.destination_start}, {self.range_length})'


class IdentityConverter(AlmanacConverter[Source, Destination]):
    def __init__(
            self,
            destination_type: type[Destination]):
        self.destination_type = destination_type

    def contains(self, source: Source) -> bool:
        return True

    def convert(self, source: Source) -> Destination:
        return self.destination_type(source.value)
    
    def __str__(self) -> str:
        return f'IdentityConverter[{self.destination_type.__name__}]'


def find_converter(
        converters: list[AlmanacConverter[Source, Destination]], 
        source: Source, 
        destination_type: type[Destination]
        ) -> AlmanacConverter[Source, Destination]:
    for converter in converters:
        if converter.contains(source):
            return converter
    return IdentityConverter[Source, Destination](destination_type)


def convert(
        input: list[str], 
        i: int, 
        sources: list[Source], 
        destination_type: type[Destination]
        ) -> tuple[list[Destination], int]:
    converters: list[AlmanacConverter[Source, Destination]] = []
    while i < len(input) and input[i] != '':
        converters.append(AlmanacConverter[Source, Destination](input[i], destination_type))
        i += 1
    converters.sort()
    destinations: list[Destination] = []
    for source in sources:
        converter = find_converter(converters, source, destination_type)
        destination = converter.convert(source)
        log(DEBUG, f'Converted {source} to {destination} using {converter}')
        destinations.append(destination)
    return destinations, i


class Part1(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        seeds = [Seed(val) for val in map(int, input[0].split(':')[1].split())]
        i = 3
        soils, i = convert(input, i, seeds, Soil)
        i += 2
        fertilizers, i = convert(input, i, soils, Fertilizer)
        i += 2
        waters, i = convert(input, i, fertilizers, Water)
        i += 2
        lights, i = convert(input, i, waters, Light)
        i += 2
        temperatures, i = convert(input, i, lights, Temperature)
        i += 2
        humidities, i = convert(input, i, temperatures, Humidity)
        i += 2
        locations, i = convert(input, i, humidities, Location)

        for i in range(len(seeds)):
            log(INFO, f'{seeds[i]}, {soils[i]}, {fertilizers[i]}, {waters[i]}, {lights[i]}, {temperatures[i]}, {humidities[i]}, {locations[i]}, ')

        min_location = min(locations)
        log(RESULT, f'The lowest locations number is: {min_location}')
        return min_location.value


part = Part1()

part.add_result(35, """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""")

part.add_result(265018614)
