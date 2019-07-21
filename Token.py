from typing import Optional
from dataclasses import dataclass
import Attack
from enum import Enum


class TokenState(Enum):
    healthy = True
    damaged = False


@dataclass
class TokenType:
    name: str
    healthy_attack: Optional[Attack.Attack]
    damaged_attack: Optional[Attack.Attack]

    def attack(self, state: TokenState):
        if state is TokenState.healthy:
            return self.healthy_attack
        elif state is TokenState.damaged:
            return self.damaged_attack
        else:
            raise RuntimeError("Invalid token state")


@dataclass
class Token:
    type: TokenType
    state: TokenState

    def fg_bg_colours(self, highlighted: bool, selected: bool):
        bg = "white" if highlighted else "black"
        if selected:
            fg = 'green'
        elif self.state is TokenState.damaged:
            fg = 'red'
        else:
            fg = "black" if highlighted else "white"
        return fg, bg

    def attack(self):
        return self.type.attack(self.state)

    def display(self, highlighted: bool, selected: bool):
        fg, bg = self.fg_bg_colours(highlighted, selected)
        return f"[color={fg}][bkcolor={bg}]{self.type.name}[/bkcolor][/color]"


HealthToken = TokenType("Health", Attack.HitAttack, None)
