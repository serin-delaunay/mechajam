from dataclasses import dataclass


@dataclass
class Attack:
    name: str
    symbol: str


HitAttack = Attack("Attack", "A")
