
def redistribute_until_loop(blocks: list[int]) -> tuple[int, int]:
    """Redistribute memory until a loop is found in the blocks, returns the start and end of the loop."""
    num_blocks = len(blocks)
    distributions: dict[int, int] = {}
    num_cycles = 0

    while hash(tuple(blocks)) not in distributions:
        distributions[hash(tuple(blocks))] = num_cycles
        max_block_size = max(blocks)
        max_block = blocks.index(max_block_size)
        blocks[max_block] = 0
        redistribute_blocks, remainder = divmod(max_block_size, num_blocks)
        for i in range(1, num_blocks + 1):
            blocks[(max_block + i) % num_blocks] += redistribute_blocks + (1 if i <= remainder else 0)
        num_cycles += 1

    return distributions[hash(tuple(blocks))], num_cycles
