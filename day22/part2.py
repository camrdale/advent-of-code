from collections import defaultdict

from aoc.input import InputParser
from aoc.log import log, RESULT, INFO
from aoc.runner import Part

from .shared import next_secret


class Part2(Part):
    def run(self, parser: InputParser) -> int:
        input = parser.get_input()

        prices: list[list[int]] = []

        for i, line in enumerate(input):
            secret = int(line)
            prices.append([secret % 10])
            for _ in range(2000):
                secret = next_secret(secret)
                prices[i].append(secret % 10)

        price_changes: list[list[int]] = []
        for i in range(len(prices)):
            price_changes.append([n - c for c, n in zip(prices[i][:-1], prices[i][1:])])

        change_sequences: list[list[tuple[int, int, int, int]]] = []
        for i in range(len(price_changes)):
            change_sequences.append([])
            for j in range(3, len(price_changes[i])):
                change_sequences[i].append((price_changes[i][j-3], price_changes[i][j-2], price_changes[i][j-1], price_changes[i][j]))

        change_sequence_results: dict[tuple[int, int, int, int], int] = defaultdict(int)
        for i in range(len(change_sequences)):
            sold_sequences: set[tuple[int, int, int, int]] = set()
            for j in range(len(change_sequences[i])):
                change_sequence = change_sequences[i][j]
                if change_sequence not in sold_sequences:
                    change_sequence_results[change_sequence] += prices[i][j+4]
                    sold_sequences.add(change_sequence)

        best_results = sorted([(result, change_sequence) for change_sequence, result in change_sequence_results.items()], reverse=True)[:10]
        log(INFO, best_results)
        log(RESULT, f'Best result {best_results[0][0]} occurs for sequence: {best_results[0][1]}')
        return best_results[0][0]


part = Part2()

part.add_result(23, """
1
2
3
2024
""")

part.add_result(1910)
