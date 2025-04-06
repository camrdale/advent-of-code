

def find_n_distinct_characters(input: str, n: int) -> int:
    """Find the position of n distinct characters in a row."""
    last_n: dict[str, int] = {}
    for i in range(len(input)):
        last_n[input[i]] = last_n.get(input[i], 0) + 1
        if i - n >= 0:
            last_n[input[i-n]] -= 1
            if last_n[input[i-n]] == 0:
                del last_n[input[i-n]]
        if len(last_n) == n:
            return i+1
    
    raise ValueError(f'Failed to find {n} distinct characters in a row')
