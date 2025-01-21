import abc


class Module(abc.ABC):
    def __init__(self):
        self.outputs: list[str] = []

    def add_input(self, input: str):
        pass

    def add_output(self, output: str):
        self.outputs.append(output)

    def send(self, pulse: bool) -> list[tuple[str, bool]]:
        send: list[tuple[str, bool]] = []
        for output in self.outputs:
            send.append((output, pulse))
        return send

    @abc.abstractmethod
    def process(self, input: str, pulse: bool) -> list[tuple[str, bool]]:
        pass


class Broadcaster(Module):
    def process(self, input: str, pulse: bool) -> list[tuple[str, bool]]:
        return self.send(pulse)


class FlipFlop(Module):
    def __init__(self):
        super().__init__()
        self.state = False

    def process(self, input: str, pulse: bool) -> list[tuple[str, bool]]:
        if pulse:
            return []
        self.state = not self.state
        return self.send(self.state)


class Conjunction(Module):
    def __init__(self):
        super().__init__()
        self.input_states: dict[str, bool] = {}

    def add_input(self, input: str):
        self.input_states[input] = False

    def process(self, input: str, pulse: bool) -> list[tuple[str, bool]]:
        self.input_states[input] = pulse
        return self.send(not all(self.input_states.values()))
