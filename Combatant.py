from typing import List, Set
from dataclasses import dataclass, field
from random import sample
from Token import Token, TokenState


def player_input(fn):
    def fn_wrapped(self, *args, **kwargs):
        if self.ai:
            return
        fn(self, *args, **kwargs)

    return fn_wrapped


@dataclass
class Combatant:
    health_tokens: List[Token]
    ai: bool = False
    active: bool = False
    highlighted_index: int = 0
    selected_indices: Set[int] = field(default_factory=set)

    def process_activations(self):
        for i in self.selected_indices:
            self.health_tokens[i].state = TokenState.healthy
        self.selected_indices.clear()

    def automate_activations(self):
        damaged_indices = [i for (i, t) in enumerate(self.health_tokens) if t.state is TokenState.damaged]
        self.selected_indices.update(sample(damaged_indices, min(self.action_points(), len(damaged_indices))))

    def display_lines(self):
        return [t.display((i == self.highlighted_index) and self.active and not self.ai, i in self.selected_indices)
                for (i, t) in enumerate(self.health_tokens)]

    def get_attacks(self):
        return sum((t.attack() for t in self.health_tokens), ())

    def action_points(self):
        return sum(t.mode().actions for t in self.health_tokens)

    @player_input
    def move_up(self):
        self.highlighted_index += len(self.health_tokens) - 1
        self.highlighted_index %= len(self.health_tokens)

    @player_input
    def move_down(self):
        self.highlighted_index += 1
        self.highlighted_index %= len(self.health_tokens)

    @player_input
    def move_left(self):
        if self.highlighted_index in self.selected_indices:
            self.selected_indices.remove(self.highlighted_index)

    @player_input
    def move_right(self):
        if len(self.selected_indices) < self.action_points():
            self.selected_indices.add(self.highlighted_index)
