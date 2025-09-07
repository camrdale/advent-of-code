import re


REQUIREMENT = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.')


class Step:
    def __init__(self, id: str, base_time: int = 60) -> None:
        self.id = id
        self.requirements: list[str] = []
        self.required_for: list[str] = []
        self.time_to_complete = base_time + ord(id) - ord('A') + 1
    
    @classmethod
    def from_input(cls, input: list[str], base_time: int = 60) -> dict[str, Step]:
        steps: dict[str, Step] = {}
        for line in input:
            match = REQUIREMENT.match(line)
            assert match is not None, line
            requirement, required_for = match.groups()
            if requirement not in steps:
                steps[requirement] = Step(requirement, base_time=base_time)
            if required_for not in steps:
                steps[required_for] = Step(required_for, base_time=base_time)
            steps[requirement].required_for.append(required_for)
            steps[required_for].requirements.append(requirement)
        return steps

    def complete(self, steps: dict[str, Step]) -> list[str]:
        """Removes edges for this completed node, returning steps that are now ready to run."""
        ready: list[str] = []
        for required_for in self.required_for:
            steps[required_for].requirements.remove(self.id)
            if not steps[required_for].requirements:
                ready.append(required_for)
        return ready
