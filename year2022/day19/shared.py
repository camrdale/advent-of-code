import enum
import functools
import math
import re
from typing import NamedTuple, Self, cast

import cachetools

MAX_CACHE_SIZE = 2000000000


BLUEPRINT = re.compile(r'Blueprint ([0-9]*): Each ore robot costs ([0-9]*) ore. Each clay robot costs ([0-9]*) ore. Each obsidian robot costs ([0-9]*) ore and ([0-9]*) clay. Each geode robot costs ([0-9]*) ore and ([0-9]*) obsidian.')


class ResourceType(enum.IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE= 3

    def __repr__(self):
        return f'{self.name}'


class Resources(NamedTuple):
    ore: int
    clay: int
    obsidian: int
    geode: int

    @classmethod
    def for_type(cls, type: ResourceType) -> Self:
        resource_list = [0]*4
        resource_list[type] = 1
        return cls(*resource_list)

    def add(self, other: 'Resources') -> 'Resources':
        return Resources(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode)

    def minus(self, other: 'Resources') -> 'Resources':
        return Resources(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geode - other.geode)
    
    def times(self, num: int) -> 'Resources':
        return Resources(
            self.ore * num,
            self.clay * num,
            self.obsidian * num,
            self.geode * num)


class Blueprint(NamedTuple):
    ore_robot: Resources
    clay_robot: Resources
    obsidian_robot: Resources
    geode_robot: Resources
    num: int

    @classmethod
    def from_match(cls, blueprint_input: tuple[str, ...]) -> Self:
        return cls(
            Resources(int(blueprint_input[1]), 0, 0, 0),
            Resources(int(blueprint_input[2]), 0, 0, 0),
            Resources(int(blueprint_input[3]), int(blueprint_input[4]), 0, 0),
            Resources(int(blueprint_input[5]), 0, int(blueprint_input[6]), 0),
            int(blueprint_input[0]))
    
    def to_build(self, type: ResourceType) -> Resources:
        return cast(Resources, self[type])
    
    @functools.cache
    def most_needed(self, resource_type: ResourceType) -> int:
        return max(self.to_build(robot_type)[resource_type] for robot_type in ResourceType)


class State(NamedTuple):
    minutes_remaining: int
    robots: Resources
    resources: Resources

    @classmethod
    def initial_state(cls, minutes: int) -> Self:
        return cls(
            minutes,
            Resources(1, 0, 0, 0),
            Resources(0, 0, 0, 0))
    
    def geodes(self) -> int:
        return self.resources.geode + (self.robots.geode * self.minutes_remaining)
    
    def build(self, build_robot: Resources, uses_resources: Resources) -> 'State | None':
        minutes_to_wait = 0
        for resource_type in ResourceType:
            if uses_resources[resource_type] > 0:
                if self.resources[resource_type] < uses_resources[resource_type]:
                    if self.robots[resource_type] == 0:
                        return None
                    minutes_to_wait = max(minutes_to_wait, math.ceil((uses_resources[resource_type] - self.resources[resource_type]) / self.robots[resource_type]))
        minutes_to_wait += 1
        if minutes_to_wait > self.minutes_remaining:
            return None
        return State(
            self.minutes_remaining - minutes_to_wait,
            self.robots.add(build_robot),
            self.resources.add(self.robots.times(minutes_to_wait)).minus(uses_resources))

    def max_resources(self, blueprint: Blueprint) -> tuple[int, int]:
        """Upper bound for how many geodes and obsidian this state could produce."""
        resources = self.resources
        robots = self.robots
        for _ in range(self.minutes_remaining):
            resources = resources._replace(geode=resources.geode + robots.geode)
            if resources.obsidian >= blueprint.geode_robot.obsidian:
                resources = resources._replace(obsidian=resources.obsidian - blueprint.geode_robot.obsidian)
                robots = robots._replace(geode=robots.geode+1)
            resources = resources._replace(obsidian=resources.obsidian + robots.obsidian)
            if resources.clay >= blueprint.obsidian_robot.clay:
                resources = resources._replace(clay=resources.clay - blueprint.obsidian_robot.clay)
                robots = robots._replace(obsidian=robots.obsidian+1)
            resources = resources._replace(clay=resources.clay + robots.clay)
            robots = robots._replace(clay=robots.clay+1, ore=robots.ore+1)
        return resources.geode, resources.obsidian + ((robots.geode - self.robots.geode) * blueprint.geode_robot.obsidian)


class GeodeMaximizer:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint
        self.cache: cachetools.LRUCache[tuple[str], int] = cachetools.LRUCache(maxsize=MAX_CACHE_SIZE)

    @cachetools.cachedmethod(lambda self: self.cache)
    def most_geodes(self, limit: int, state: State) -> int:
        max_geodes = 0
        for build_next in reversed(list(ResourceType)):
            if build_next != ResourceType.GEODE and state.robots[build_next] >= self.blueprint.most_needed(build_next):
                continue
            geodes = state.geodes()
            build_resources = self.blueprint.to_build(build_next)
            new_state = state.build(Resources.for_type(build_next), build_resources)
            if new_state is not None:
                max_resources = new_state.max_resources(self.blueprint)
                if max_resources[1] < self.blueprint.geode_robot.obsidian:
                    # Abort early if there will never be enough obsidian to build more geode robots
                    geodes = new_state.geodes()
                elif max_resources[0] > max(limit, max_geodes):
                    geodes = self.most_geodes(max_geodes, new_state)
            
            if geodes > max_geodes:
                max_geodes = geodes
        return max_geodes
