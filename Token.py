from typing import Optional
from dataclasses import dataclass
import Attack


@dataclass
class Token:
    name: str
    attack: Optional[Attack.Attack] = None


HealthToken = Token("Health", Attack.HitAttack)
