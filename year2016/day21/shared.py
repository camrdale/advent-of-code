import re


OPERATION = re.compile(
    r'(swap|reverse|rotate|move) (position|letter|positions|left|right|based on position of letter) ([a-z0-9])( with position | with letter | steps| through | to position )?([a-z0-9])?')


def rotate_based_on_position(scram: list[str], c: str) -> list[str]:
    n = 1 + scram.index(c)
    if n >= 5:
        n += 1
    n %= len(scram)
    return scram[-n:] + scram[:-n]


def apply_operation(line: str, scram: list[str], reverse: bool = False) -> None:
    op = OPERATION.match(line)
    assert op, line

    match op.group(1):
        case 'swap':
            if op.group(2) == 'position':
                p1 = int(op.group(3))
                p2 = int(op.group(5))
            else:
                p1 = scram.index(op.group(3))
                p2 = scram.index(op.group(5))
            scram[p1], scram[p2] = scram[p2], scram[p1]
        case 'rotate':
            if op.group(2) == 'based on position of letter':
                if not reverse:
                    scram[:] = rotate_based_on_position(scram, op.group(3))
                    return
                for n in range(len(scram)):
                    if rotate_based_on_position(scram[n:] + scram[:n], op.group(3)) == scram:
                        scram[:] = scram[n:] + scram[:n]
                        return
            if op.group(2) == 'right':
                n = int(op.group(3))
            elif op.group(2) == 'left':
                n = len(scram) - int(op.group(3))
            else:
                raise ValueError(f'{line}: {op.groups()}')
            n %= len(scram)
            scram[:] = scram[n if reverse else -n:] + scram[:n if reverse else -n]
        case 'reverse':
            p1 = int(op.group(3))
            p2 = int(op.group(5))
            scram[:] = scram[:p1] + scram[p2:p1-1 if p1 > 0 else None:-1] + scram[p2+1:]
        case 'move':
            p1 = int(op.group(3))
            p2 = int(op.group(5))
            c = scram.pop(p2 if reverse else p1)
            scram.insert(p1 if reverse else p2, c)
        case _:
            raise ValueError(f'{line}: {op.groups()}')
