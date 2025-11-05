
def from_binary_space(seat: str) -> int:
    return int(seat.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2)
