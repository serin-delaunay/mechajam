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

    def attack(self):
        return self.type.attack(self.state)

    def __str__(self):
        colour = "white" if self.state is TokenState.healthy else "red"
        return f"[color={colour}]{self.type.name}[/color]"


HealthToken = TokenType("Health", Attack.HitAttack, None)
