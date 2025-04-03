from typing import NamedTuple


class ItemType(NamedTuple):
    identifier: str

    def priority(self) -> int:
        if 'a' <= self.identifier <= 'z':
            return ord(self.identifier) - ord('a') + 1
        return ord(self.identifier) - ord('A') + 27

    def __repr__(self) -> str:
        return self.identifier


class Rucksack(NamedTuple):
    supplies: list[ItemType]

    @classmethod
    def from_text(cls, text: str) -> 'Rucksack':
        return cls([ItemType(c) for c in text])
    
    def first_compartment(self) -> list[ItemType]:
        assert len(self.supplies) % 2 == 0
        return self.supplies[:(len(self.supplies)//2)]
    
    def second_compartment(self) -> list[ItemType]:
        assert len(self.supplies) % 2 == 0
        return self.supplies[(len(self.supplies)//2):]
    
    def in_both_compartments(self) -> ItemType:
        first_compartment_items = set(self.first_compartment())
        second_compartment_items = set(self.second_compartment())
        in_both = first_compartment_items.intersection(second_compartment_items)
        assert len(in_both) == 1
        return next(iter(in_both))
    
    def group_badge(self, second_elf: 'Rucksack', third_elf: 'Rucksack') -> ItemType:
        badge = set(self.supplies) & set(second_elf.supplies) & set(third_elf.supplies)
        assert len(badge) == 1
        return next(iter(badge))

    def __repr__(self) -> str:
        return ''.join(str(i) for i in self.supplies)
