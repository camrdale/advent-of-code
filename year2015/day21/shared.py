from typing import NamedTuple, Self


class Item(NamedTuple):
    name: str
    cost: int
    damage: int
    armor: int


WEAPONS = [
    Item('Dagger', 8, 4, 0),
    Item('Shortsword', 10, 5, 0),
    Item('Warhammer', 25, 6, 0),
    Item('Longsword', 40, 7, 0),
    Item('Greataxe', 74, 8, 0)]
ARMORS = [
    Item('None', 0, 0, 0),
    Item('Leather', 13, 0, 1),
    Item('Chainmail', 31, 0, 2),
    Item('Splintmail', 53, 0, 3),
    Item('Bandedmail', 75, 0, 4),
    Item('Platemail', 102, 0, 5)]
RINGS = [
    Item('None 1', 0, 0, 0),
    Item('None 2', 0, 0, 0),
    Item('Damage +1', 25, 1, 0),
    Item('Damage +2', 50, 2, 0),
    Item('Damage +3', 100, 3, 0),
    Item('Defense +1', 20, 0, 1),
    Item('Defense +2', 40, 0, 2),
    Item('Defense +3', 80, 0, 3)]


class Loadout(NamedTuple):
    weapon: Item
    armor_item: Item
    ring_1: Item
    ring_2: Item

    def cost(self) -> int:
        return sum(item.cost for item in self)

    def damage(self) -> int:
        return sum(item.damage for item in self)

    def armor(self) -> int:
        return sum(item.armor for item in self)


def all_loadouts() -> list[Loadout]:
    loadouts: list[Loadout] = []
    for weapon in WEAPONS:
        for armor in ARMORS:
            for i, ring_1 in enumerate(RINGS[:-1]):
                for ring_2 in RINGS[i+1:]:
                    loadouts.append(Loadout(weapon, armor, ring_1, ring_2))

    loadouts.sort(key=Loadout.cost)
    return loadouts


class Character:
    def __init__(self, hp: int, damage: int, armor: int) -> None:
        self.starting_hp = hp
        self.hp = hp
        self.damage = damage
        self.armor = armor

    @classmethod
    def from_loadout(cls, hp: int, loadout: Loadout) -> Self:
        return cls(hp, loadout.damage(), loadout.armor())

    @classmethod
    def from_input(cls, input: list[str]) -> Self:
        return cls(
            int(input[0].split(':')[1]),
            int(input[1].split(':')[1]),
            int(input[2].split(':')[1]))

    def attacked(self, other: 'Character') -> bool:
        """Character is being attacked by other character. Returns True if this character dies."""
        damage = other.damage - self.armor
        if damage < 1:
            damage = 1
        self.hp -= damage
        if self.hp <= 0:
            return True
        return False

    def reset(self) -> None:
        self.hp = self.starting_hp


def fight(player: Character, boss: Character) -> bool:
    """Returns True if player beats the boos."""
    while True:
        if boss.attacked(player):
            return True
        if player.attacked(boss):
            return False
