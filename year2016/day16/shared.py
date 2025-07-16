def dragon_curve(size: int, data: list[int]):
    if len(data) >= size:
        del data[size:]
        return
    data.extend([0] + [1 - b for b in data[::-1]])
    dragon_curve(size, data)


def dragon_checksum(data: list[int]) -> list[int]:
    if len(data) % 2 != 0:
        return data
    next_data: list[int] = []
    for i in range(0, len(data), 2):
        next_data.append(1 if data[i] == data[i+1] else 0)
    return dragon_checksum(next_data)
