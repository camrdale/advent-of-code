import re

from aoc.input import InputParser
from aoc import log
from aoc.runner import Part


YEAR = re.compile(r'([0-9]{4})')
HEIGHT = re.compile(r'([0-9]*)(in|cm)')
HAIR_COLOR =re.compile(r'#[0-9a-f]{6}')
EYE_COLOR = re.compile(r'(amb|blu|brn|gry|grn|hzl|oth)')
ID = re.compile(r'[0-9]{9}')


def is_valid(fields: dict[str, str]) -> bool:
    for key, value in fields.items():
        match key:
            case 'byr' | 'iyr' | 'eyr':
                match = YEAR.fullmatch(value)
                if match is None:
                    return False
                years = int(match.group(1))
                if key == 'byr' and (years < 1920 or years > 2002):
                    return False
                if key == 'iyr' and (years < 2010 or years > 2020):
                    return False
                if key == 'eyr' and (years < 2020 or years > 2030):
                    return False
            case 'hgt':
                match = HEIGHT.fullmatch(value)
                if match is None:
                    return False
                height = int(match.group(1))
                if match.group(2) == 'cm' and (height < 150 or height > 193):
                    return False
                elif match.group(2) == 'in' and (height < 59 or height > 76):
                    return False
            case 'hcl':
                match = HAIR_COLOR.fullmatch(value)
                if match is None:
                    return False
            case 'ecl':
                match = EYE_COLOR.fullmatch(value)
                if match is None:
                    return False
            case 'pid':
                match = ID.fullmatch(value)
                if match is None:
                    return False
            case 'cid':
                pass
            case _:
                raise ValueError(f'Unexpected key: {key}')
    return True


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_multipart_input()

        required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
        valid = 0
        for part in input:
            fields: dict[str, str] = dict(field.split(':') for line in part for field in line.split())
            if required_fields.issubset(fields.keys()) and is_valid(fields):
                valid += 1

        log.log(log.RESULT, f'The number of valid passwords: {valid}')
        return valid


part = Part2()

part.add_result(0, """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
""")

part.add_result(4, """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
""")

part.add_result(172)
