import graphviz

import cachetools


MAX_CACHE_SIZE = 1_000_000


class Device:
    def __init__(self, name: str) -> None:
        self.name = name
        self.outputs: list[Device] = []
        self.cache: cachetools.LRUCache[tuple[str], int] = cachetools.LRUCache(maxsize=MAX_CACHE_SIZE)

    @classmethod
    def from_input(cls, lines: list[str]) -> dict[str, Device]:
        dot = graphviz.Digraph(name='devices')
        devices: dict[str, Device] = {}
        for line in lines:
            device_name, output_names = line.split(': ')
            if device_name not in devices:
                dot.node(device_name)
                devices[device_name] = Device(device_name)
            for output_name in output_names.split():
                if output_name not in devices:
                    dot.node(output_name)
                    devices[output_name] = Device(output_name)
                devices[device_name].add_output(devices[output_name])
                dot.edge(device_name, output_name)
        # dot.render()
        return devices
    
    def add_output(self, output: Device):
        self.outputs.append(output)

    @cachetools.cachedmethod(lambda self: self.cache)
    def paths_to_out(self) -> int:
        if self.name == 'out':
            return 1
        return sum(output.paths_to_out() for output in self.outputs)

    @cachetools.cachedmethod(lambda self: self.cache)
    def paths_to_out_through_fft_and_dac(self, seen_fft: bool, seen_dac: bool) -> int:
        if self.name == 'out':
            return 1 if (seen_fft and seen_dac) else 0
        if self.name == 'fft':
            seen_fft = True
        if self.name == 'dac':
            seen_dac = True
        return sum(output.paths_to_out_through_fft_and_dac(seen_fft, seen_dac) for output in self.outputs)
