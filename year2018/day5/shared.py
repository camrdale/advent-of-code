def reacts(a: str, b: str) -> bool:
    return a.islower() != b.islower() and a.lower() == b.lower()


def react(polymer: str) -> str:
    units: list[str] = []
    for c in polymer:
        if units and reacts(units[-1], c):
            units.pop()
        else:
            units.append(c)
    return ''.join(units)
