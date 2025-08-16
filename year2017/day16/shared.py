def dance(initial_order: str, moves: str) -> str:
    programs = list(initial_order)
    for move in moves.split(','):
        match move[0]:
            case 's':
                spin = int(move[1:])
                programs = programs[-spin:] + programs[:-spin]
            case 'x':
                swap1, swap2 = map(int, move[1:].split('/'))
                programs[swap1], programs[swap2] = programs[swap2], programs[swap1]
            case 'p':
                swap1 = programs.index(move[1])
                swap2 = programs.index(move[3])
                programs[swap1], programs[swap2] = programs[swap2], programs[swap1]
            case _:
                raise ValueError(f'Failed to parse dance move: {move}')
    return ''.join(programs)
