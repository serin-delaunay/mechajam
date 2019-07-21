from typing import List, Set
from dataclasses import dataclass, field
from Token import Token


@dataclass
class Combatant:
    health_tokens: List[Token]
    active: bool = False
    highlighted_index: int = 0
    selected_indices: Set[int] = field(default_factory=set)

    def display_lines(self):
        return [t.display((i == self.highlighted_index) and self.active)
                for (i, t) in enumerate(self.health_tokens)]

    def get_attacks(self):
        return [a for a in (token.attack() for token in self.health_tokens) if a is not None]
