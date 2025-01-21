import collections
import queue

import aoc.input
from aoc import log
from aoc import runner

from year2023.day20 import shared


class Modules:
    def __init__(self):
        self.modules: dict[str, shared.Module] = {}
    
    def add_module(self, module_name: str, module: shared.Module):
        self.modules[module_name] = module
    
    def connect_modules(self, module_name: str, output_name: str):
        self.modules[module_name].add_output(output_name)
        if output_name in self.modules:
            self.modules[output_name].add_input(module_name)
    
    def broadcast(self, pulse: bool) -> dict[bool, int]:
        pulses = {False: 0, True: 0}
        to_send: queue.SimpleQueue[tuple[str, str, bool]] = queue.SimpleQueue()

        broadcaster = self.modules['broadcaster']
        for sent in broadcaster.process('button', pulse):
            to_send.put(('broadcaster',) + sent)
        pulses[pulse] += 1

        while not to_send.empty():
            input_name, module_name, pulse = to_send.get()
            if module_name in self.modules:
                module = self.modules[module_name]
                for sent in module.process(input_name, pulse):
                    to_send.put((module_name,) + sent)
            pulses[pulse] += 1

        return pulses


class Part1(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        modules = Modules()
        for line in input:
            module_name = line.split()[0]
            if module_name == 'broadcaster':
                modules.add_module(module_name, shared.Broadcaster())
            elif module_name.startswith('&'):
                modules.add_module(module_name[1:], shared.Conjunction())
            else:
                modules.add_module(module_name[1:], shared.FlipFlop())
        
        for line in input:
            module_names = line.split()
            module_name = module_names[0].lstrip('%&')
            for output_name in module_names[2:]:
                output_name = output_name.rstrip(',')
                modules.connect_modules(module_name, output_name)
        
        counter: collections.Counter[bool] = collections.Counter()
        for _ in range(1000):
            counter.update(modules.broadcast(False))

        result = counter[True] * counter[False]
        log.log(log.RESULT, f'Multiplying the total number of low pulses sent by the total number of high pulses sent: {result}')
        return result


part = Part1()

part.add_result(32000000, r"""
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""")

part.add_result(11687500, r"""
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""")

part.add_result(763500168)
