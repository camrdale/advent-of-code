from typing import NamedTuple, Self


class Component(NamedTuple):
    port_a: int
    port_b: int

    @classmethod
    def from_text(cls, text: str) -> Self:
        return cls(*map(int, text.split('/')))
    
    def strength(self) -> int:
        return self.port_a + self.port_b
    
    def other_port(self, port: int) -> int:
        if port == self.port_a:
            return self.port_b
        return self.port_a
