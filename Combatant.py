from typing import List, Set
from dataclasses import dataclass, field
from Token import Token, TokenState


@dataclass
class Combatant:
    health_tokens: List[Token]
    active: bool = False
    highlighted_index: int = 0
    selected_indices: Set[int] = field(default_factory=set)

    def process_activations(self):
        for i in self.selected_indices:
            self.health_tokens[i].state = TokenState.healthy
        self.selected_indices.clear()

    def display_lines(self):
        return [t.display((i == self.highlighted_index) and self.active, i in self.selected_indices)
                for (i, t) in enumerate(self.health_tokens)]

    def get_attacks(self):
        return [a for a in (token.attack() for token in self.health_tokens) if a is not None]

    def move_up(self):
        self.highlighted_index += len(self.health_tokens) - 1
        self.highlighted_index %= len(self.health_tokens)

    def move_down(self):
        self.highlighted_index += 1
        self.highlighted_index %= len(self.health_tokens)

    def move_left(self):
        if self.highlighted_index in self.selected_indices:
            self.selected_indices.remove(self.highlighted_index)

    def move_right(self):
        self.selected_indices.add(self.highlighted_index)
