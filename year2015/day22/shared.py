import functools
from typing import NamedTuple, Self

from aoc import log


PLAYER_WINS = 1
BOSS_WINS = 2


class Spell(NamedTuple):
    name: str
    cost: int
    effect_duration: int
    damage: int
    heal: int
    armor: int
    mana: int


SPELLS = [
    Spell('Magic Missile', 53, 0, 4, 0, 0, 0),
    Spell('Drain', 73, 0, 2, 2, 0, 0),
    Spell('Shield', 113, 6, 0, 0, 7, 0),
    Spell('Poison', 173, 6, 3, 0, 0, 0),
    Spell('Recharge', 229, 5, 0, 0, 0, 101),
]


class GameState(NamedTuple):
    player_hp: int
    mana: int
    boss_hp: int
    boss_damage: int
    effects: frozenset[Spell]
    winner: int

    @classmethod
    def initial(cls, input: list[str]) -> Self:
        return cls(
            50, 500,
            int(input[0].split(':')[1]),
            int(input[1].split(':')[1]),
            frozenset(), 0)

    def apply_spell(self, spell: Spell) -> 'GameState':
        effects = self.effects
        if spell in self.effects:
            effects = effects - {spell}
            if spell.effect_duration > 1:
                effects = effects | {spell._replace(effect_duration=spell.effect_duration - 1)}
        
        return GameState(
            self.player_hp + spell.heal,
            self.mana + spell.mana,
            self.boss_hp - spell.damage,
            self.boss_damage,
            effects,
            PLAYER_WINS if self.boss_hp - spell.damage <= 0 else 0)

    def process_effects(self) -> 'GameState':
        state = self
        for spell in self.effects:
            state = state.apply_spell(spell)
            if state.winner:
                return state
        return state
    
    def boss_attack(self) -> 'GameState':
        damage = max(1, self.boss_damage - sum(effect.armor for effect in self.effects))
        player_hp = self.player_hp - damage
        return self._replace(player_hp=player_hp, winner=BOSS_WINS if player_hp <= 0 else 0)

    def hard_difficulty(self) -> 'GameState':
        return self._replace(player_hp=self.player_hp - 1, winner=(BOSS_WINS if self.player_hp <= 1 else 0))

    def next_state(self, spell: Spell, hard: bool) -> 'GameState':
        if spell.name in [effect.name for effect in self.effects]:
            raise ValueError(f'Cannot cast {spell.name}, it is still active: {self.effects}')
        if spell.cost > self.mana:
            raise ValueError(f'Cannot cast {spell.name}, it costs more than the {self.mana} mana player has')

        state = self._replace(mana=self.mana - spell.cost)
        if spell.effect_duration > 0:
            state = state._replace(effects=self.effects | {spell})
        else:
            state = state.apply_spell(spell)

        if state.winner:
            return state
        
        state = state.process_effects()
        if state.winner:
            return state

        state = state.boss_attack()
        if state.winner:
            return state
        
        if hard:
            state = state.hard_difficulty()
            if state.winner:
                return state

        state = state.process_effects()
        return state


@functools.cache
def min_mana_to_win(state: GameState, hard: bool = False, remaining_mana: int | None = None) -> int | None:
    log.log(log.DEBUG, f'{remaining_mana}: {state}')
    if state.winner:
        if state.winner == PLAYER_WINS:
            return 0
        else:
            return None

    if remaining_mana is not None and remaining_mana < 0:
        return None

    min_mana = remaining_mana
    for spell in SPELLS:
        if spell.name in [effect.name for effect in state.effects]:
            continue
        if spell.cost > state.mana:
            continue

        next_remaining_mana = None
        if min_mana is not None:
            next_remaining_mana = min_mana - spell.cost
        if next_remaining_mana is not None and next_remaining_mana < 0:
            continue

        mana = min_mana_to_win(state.next_state(spell, hard), hard=hard, remaining_mana=next_remaining_mana)
        if mana is not None and (min_mana is None or spell.cost + mana < min_mana):
            min_mana = spell.cost + mana

            if remaining_mana is None or min_mana < remaining_mana:
                log.log(log.INFO, f'New min {min_mana} for: {state}')
    
    return min_mana
