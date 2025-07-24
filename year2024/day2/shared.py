class Report:
    """A report containing a list of the levels observed."""

    def __init__(self, levels: list[int]) -> None:
        self.levels = levels

    def __eq__(self, other: object) -> bool:
        if type(other) != Report:
            return False
        return tuple(self.levels) == tuple(other.levels)
    
    def __hash__(self) -> int:
        return hash((tuple(self.levels)))
    
    def deltas(self) -> list[int]:
        """Get a list of the changes in the levels."""
        return [self.levels[i] - self.levels[i-1] for i in range(1, len(self.levels))]
    
    def normalize(self) -> 'Report':
        """Normalize the levels to prefer increasing (reverses if decreasing)."""
        num_increasing = len([d for d in self.deltas() if d > 0])
        num_decreasing = len([d for d in self.deltas() if d < 0])
        if num_increasing < num_decreasing:
            normalized = list(self.levels)
            normalized.reverse()
            return Report(normalized)
        return self

    def safe(self) -> bool:
        """Check if the levels are safely increasing/decreasing."""
        deltas = self.deltas()
        return max(deltas) <= 3 and min(deltas) > 0

    def dampen(self) -> 'Report':
        """Dampen the report by removing at most one level."""
        deltas = self.deltas()
        dampened = list(self.levels)
        for i in range(len(deltas)):
            if deltas[i] <= 0 or deltas[i] > 3:
                if i+1 == len(deltas):
                    # Drop the last level/delta in a report
                    del dampened[i+1]
                elif 0 < deltas[i] + deltas[i+1] <= 3:
                    # Safe to add the delta to the following one.
                    del dampened[i+1]
                elif i != 0:
                    # Fallback to try adding the delta to the previous one
                    del dampened[i]
                else:
                    # i is 0 so the first level/delta in the report is dropped.
                    del dampened[i]
                break
        return Report(dampened)
