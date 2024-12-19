import cachetools

MAX_CACHE_SIZE = 2000000


class Towels:

    def __init__(self, input: str):
        self.towels = frozenset(input.strip().split(', '))
        self.max_length = max(len(towel) for towel in self.towels)
        self.cache: cachetools.LRUCache[tuple[str], int] = cachetools.LRUCache(maxsize=MAX_CACHE_SIZE)

    @cachetools.cachedmethod(lambda self: self.cache)
    def build_design(self, design: str) -> int:
        """Try to build the design using these towels, returns the number of possible ways to do so."""
        if len(design) == 0:
            return 1
        
        num_possibilities: int = 0
        for l in range(self.max_length, 0, -1):
            if len(design) >= l and design[:l] in self.towels:
                # print('Trying', design[:l], 'remaining:', design[l:])
                num_possibilities += self.build_design(design[l:])

        # print(f'{num_possibilities} for design {design}')
        return num_possibilities
