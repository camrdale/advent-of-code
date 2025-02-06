from typing import Any

from aoc import log


class OrbitalObject:
    def __init__(self, name: str):
        self.name = name
        self.orbits: OrbitalObject
        self.orbitted_by: set[OrbitalObject] = set()
        self.depth: int

    def add_orbitted_by(self, orbitted_by: 'OrbitalObject'):
        self.orbitted_by.add(orbitted_by)

    def __eq__(self, other: Any) -> bool:
        if type(other) != OrbitalObject:
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


def build_tree(input: list[str]) -> dict[str, OrbitalObject]:
    objects: dict[str, OrbitalObject] = {}
    for line in input:
        orbital_object_name, orbitted_by_name = line.split(')')
        if orbital_object_name not in objects:
            objects[orbital_object_name] = OrbitalObject(orbital_object_name)
        if orbitted_by_name not in objects:
            objects[orbitted_by_name] = OrbitalObject(orbitted_by_name)
        objects[orbital_object_name].add_orbitted_by(objects[orbitted_by_name])
        objects[orbitted_by_name].orbits = objects[orbital_object_name]

    log.log(log.DEBUG, f'Built a tree with {len(objects)} nodes')

    objects['COM'].depth = 0
    to_process = [objects['COM']]
    total_depth = 0
    while to_process:
        orbital_object = to_process.pop()
        total_depth += orbital_object.depth
        for orbitted_by in orbital_object.orbitted_by:
            orbitted_by.depth = orbital_object.depth + 1
            to_process.append(orbitted_by)

    return objects
