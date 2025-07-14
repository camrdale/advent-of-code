import collections
import concurrent.futures
import hashlib
import re

from aoc import log


TRIPLE = re.compile(r'(.)\1{2,}')
QUINTUPLE = re.compile(r'(.)\1{4,}')

INDEX_MAX = 30000
INDEXES_PER_PROCESS = 1000


def stretched_hash(prefix: str, stretch_count: int, index_start: int) -> tuple[list[tuple[str, int]], list[tuple[int, str]]]:
    triples: list[tuple[str, int]] = []
    quintuples: list[tuple[int, str]] = []
    prefix_hash = hashlib.md5(prefix.encode())

    for index in range(index_start, index_start + INDEXES_PER_PROCESS):
        hash = prefix_hash.copy()
        hash.update(f'{index}'.encode())
        digest = hash.hexdigest()
        for _ in range(stretch_count):
            digest = hashlib.md5(digest.encode()).hexdigest()
        if match := QUINTUPLE.search(digest):
            quintuples.append((index, match.group(1)))
        if match := TRIPLE.search(digest):
            triples.append((match.group(1), index))
    return triples, quintuples


class QuintupleHasher:
    def __init__(self, prefix: str, stretch_count: int = 0) -> None:
        self.prefix = prefix
        self.stretch_count = stretch_count

    def keys(self, progress_bar: log.ProgressBar | None = None) -> set[int]:
        all_triples: dict[str, list[int]] = collections.defaultdict(list)
        all_quintuples: list[tuple[int, str]] = []

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for triples, quintuples in executor.map(
                    stretched_hash,
                    [self.prefix for _ in range(0, INDEX_MAX, INDEXES_PER_PROCESS)],
                    [self.stretch_count for _ in range(0, INDEX_MAX, INDEXES_PER_PROCESS)],
                    range(0, INDEX_MAX, INDEXES_PER_PROCESS)):
                for c, index in triples:
                    all_triples[c].append(index)
                all_quintuples.extend(quintuples)

        all_quintuples.sort()

        keys: set[int] = set()
        for index, c in all_quintuples:
            new_keys = [i for i in all_triples[c] if index > i >= index - 1000]
            log.log(log.INFO, f'Found quintuple "{c}" from MD5 hash of "{self.prefix}{index}" giving keys: {new_keys}')
            keys.update(new_keys)
            if len(keys) >= 64 and sorted(keys)[63] < index - 1000:
                break

        if len(keys) < 64:
            raise ValueError(f'Failed to find 64 keys in first {INDEX_MAX} hashes, increase INDEX_MAX')
        return keys
