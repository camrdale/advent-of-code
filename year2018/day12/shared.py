from aoc import log


class Plants:
    def __init__(self, initial_state: str, spread_input: list[str]) -> None:
        self.generation = 0
        self.state = initial_state
        self.leftmost_index = 0
        self.spread: dict[str, str] = {}
        for line in spread_input:
            note, result = line.split(' => ')
            self.spread[note] = result

    def sum_plant_indices(self) -> int:
        sum_indices = 0
        count_indices = 0
        for i, c in enumerate(self.state):
            if c == '#':
                sum_indices += i
                count_indices += 1
        return count_indices * self.leftmost_index + sum_indices

    def next_generation(self) -> None:
        state = '.....' + self.state + '.....'

        i = 0
        next_state = '..'
        while i + 5 <= len(state):
            next_state += self.spread.get(state[i:i+5], '.')
            i += 1
        
        lindex = next_state.index('#')
        rindex = next_state.rindex('#')

        self.generation += 1
        self.state = next_state[lindex:rindex+1]
        self.leftmost_index += lindex - 5
        log.log(log.INFO, self.generation, self.state, self.leftmost_index)

    def advance_to(self, generation: int) -> None:
        while True:
            old_state = self.state
            old_leftmost_index = self.leftmost_index
            self.next_generation()
            if self.generation == generation:
                return
            if self.state == old_state:
                break

        delta_leftmost_index = self.leftmost_index - old_leftmost_index
        self.leftmost_index += (generation - self.generation) * delta_leftmost_index
        self.generation = generation
