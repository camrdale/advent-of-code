from enum import IntEnum
import re
import sys
from typing import NamedTuple, Any


GROUP = re.compile(r'([0-9]*) units each with ([0-9]*) hit points (?:[ \(;\)]*(immune|weak) to ([a-z ,]*))?[ \(;\)]*(?:(immune|weak) to ([a-z ,]*)[ \(;\)]*)?with an attack that does ([0-9]*) ([a-z]*) damage at initiative ([0-9]*)')


class UnitType(IntEnum):
    IMMUNE_SYSTEM = 0
    INFECTION = 1


class Unit:
    def __init__(self, type: UnitType, text: str, boost: int = 0) -> None:
        self.type = type
        match = GROUP.match(text)
        assert match is not None, text
        self.units = int(match.group(1))
        self.hit_points = int(match.group(2))
        self.immunities: list[str] = []
        self.weaknesses: list[str] = []
        self.parse_weaknesses_immunities(match.group(3), match.group(4))
        self.parse_weaknesses_immunities(match.group(5), match.group(6))
        self.attack_damage = int(match.group(7)) + boost
        self.attack_type = match.group(8)
        self.initiative = int(match.group(9))

    def parse_weaknesses_immunities(self, type: str | None, value: str) -> None:
        match type:
            case 'immune':
                self.immunities = value.split(', ')
            case 'weak':
                self.weaknesses = value.split(', ')
            case _:
                pass

    def effective_power(self) -> int:
        return self.units * self.attack_damage
    
    def damage(self, defender: Unit) -> int:
        if self.attack_type in defender.immunities:
            return 0
        damage = self.effective_power()
        if self.attack_type in defender.weaknesses:
            damage *= 2
        return damage
    
    def targeting_order_key(self) -> tuple[int, int]:
        return -self.effective_power(), -self.initiative

    def attack_targeting_key(self, defender: Unit) -> tuple[int, int, int]:
        """Sorts defenders such that preferred targets are last."""
        return self.damage(defender), defender.effective_power(), defender.initiative
    
    def choose_target(self, defenders: list[Unit]) -> Unit | None:
        max_key = (0, sys.maxsize, sys.maxsize)
        max_key_defender: Unit | None = None
        for defender in defenders:
            key = self.attack_targeting_key(defender)
            if key > max_key:
                max_key = key
                max_key_defender = defender
        return max_key_defender

    def __lt__(self, other: Any) -> bool:
        """Default sort by targeting order."""
        if type(other) != Unit:
            raise ValueError(f'Unexpected {other}')
        return self.targeting_order_key() < other.targeting_order_key()


class Attack(NamedTuple):
    attacker: Unit
    defender: Unit

    def __lt__(self, other: Any) -> bool:
        """Default sort by descending initiative order of attackers."""
        if type(other) != Attack:
            raise ValueError(f'Unexpected {other}')
        return self.attacker.initiative >= other.attacker.initiative
    
    def attack(self) -> int:
        """Perform the attack, returns the number of units killed."""
        if self.attacker.units <= 0:
            return 0
        damage = self.attacker.damage(self.defender)
        units_killed = damage // self.defender.hit_points
        self.defender.units -= units_killed
        return units_killed


class ImmuneSystemSimulator:
    def __init__(self, immune_groups: list[str], infection_groups: list[str], immune_boost: int = 0):
        self.immune_groups: list[Unit] = []
        for group_text in immune_groups:
            self.immune_groups.append(Unit(UnitType.IMMUNE_SYSTEM, group_text, boost=immune_boost))
        self.infection_groups: list[Unit] = []
        for group_text in infection_groups:
            self.infection_groups.append(Unit(UnitType.INFECTION, group_text))
        self.rounds = 0
    
    def groups(self, unit_type: UnitType) -> list[Unit]:
        match unit_type:
            case UnitType.IMMUNE_SYSTEM:
                return self.immune_groups
            case UnitType.INFECTION:
                return self.infection_groups

    def combat(self) -> None:
        """Run all the rounds of combat."""
        while self.immune_groups and self.infection_groups:
            attacks = self.target(self.immune_groups, self.infection_groups)
            attacks.extend(self.target(self.infection_groups, self.immune_groups))
            attacks.sort()
            total_units_killed = 0
            for attack in attacks:
                total_units_killed += attack.attack()
                if attack.defender.units <= 0:
                    self.groups(attack.defender.type).remove(attack.defender)
            self.rounds += 1
            if total_units_killed == 0:
                # Stalemate, the groups don't have enough remaining attack power to kill any units.
                break

    def target(self, attacking_groups: list[Unit], defending_groups: list[Unit]) -> list[Attack]:
        attacks: list[Attack] = []
        attacking_groups.sort()
        defenders = list(defending_groups)
        for attacker in attacking_groups:
            if not defenders:
                break
            defender = attacker.choose_target(defenders)
            if defender is not None:
                defenders.remove(defender)
                attacks.append(Attack(attacker, defender))
        return attacks

    def remaining_units(self) -> int:
        return (
            sum(unit.units for unit in self.immune_groups if unit.units > 0) + 
            sum(unit.units for unit in self.infection_groups if unit.units > 0))
