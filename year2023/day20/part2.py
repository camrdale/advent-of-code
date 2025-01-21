import math
import queue

import graphviz

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
    
    def broadcast(self, pulse: bool) -> set[str]:
        """Returns all modules sending a high value during the broadcast."""
        pulses: set[str] = set()
        to_send: queue.SimpleQueue[tuple[str, str, bool]] = queue.SimpleQueue()

        broadcaster = self.modules['broadcaster']
        for sent in broadcaster.process('button', pulse):
            to_send.put(('broadcaster',) + sent)
        if pulse:
            pulses.add('button')

        while not to_send.empty():
            input_name, module_name, pulse = to_send.get()
            if module_name in self.modules:
                module = self.modules[module_name]
                for sent in module.process(input_name, pulse):
                    if sent[1]:
                        pulses.add(module_name)
                    to_send.put((module_name,) + sent)

        return pulses


class Part2(runner.Part):
    def run(self, parser: aoc.input.InputParser) -> int:
        input = parser.get_input()

        dot = graphviz.Digraph(name='modules')
        module_name_mappings: dict[str, str] = {}

        modules = Modules()
        for line in input:
            module_name = line.split()[0]
            dot.node(module_name.replace('%', r'\%'))
            if module_name == 'broadcaster':
                modules.add_module(module_name, shared.Broadcaster())
                module_name_mappings[module_name] = module_name
            elif module_name.startswith('&'):
                modules.add_module(module_name[1:], shared.Conjunction())
                module_name_mappings[module_name[1:]] = module_name.replace('%', r'\%')
            else:
                modules.add_module(module_name[1:], shared.FlipFlop())
                module_name_mappings[module_name[1:]] = module_name.replace('%', r'\%')

        dot.node(r'\%rx')
        module_name_mappings['rx'] = r'\%rx'

        dh_inputs: set[str] = set()
        for line in input:
            module_names = line.split()
            module_name = module_names[0].lstrip('%&')
            for output_name in module_names[2:]:
                output_name = output_name.rstrip(',')
                modules.connect_modules(module_name, output_name)
                dot.edge(module_name_mappings[module_name], module_name_mappings[output_name])
                if output_name == 'dh':
                    dh_inputs.add(module_name)

        dot.render()

        dh_inputs_first_high = {dh_input: 0 for dh_input in dh_inputs}
        i = 0
        while True:
            i += 1
            pulses = modules.broadcast(False)
            if pulses.intersection(dh_inputs):
                for dh_input in pulses.intersection(dh_inputs):
                    if dh_inputs_first_high[dh_input] == 0:
                        dh_inputs_first_high[dh_input] = i
                        log.log(log.INFO, f'dh input received first high signal from {dh_input} after {i} button presses')
                if all(dh_inputs_first_high.values()):
                    break

        dh_first_low = math.lcm(*dh_inputs_first_high.values())
        log.log(log.RESULT, f'"rx" received low signal after {dh_first_low} button presses')
        return dh_first_low


part = Part2()

part.add_result(207652583562007)
