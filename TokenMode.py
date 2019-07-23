from dataclasses import dataclass
from typing import Tuple
import Data
import Attack


@dataclass
class TokenMode:
    attacks: Tuple[Attack.Attack] = ()
    actions: int = 0

    @classmethod
    def from_json(cls, **kwargs):
        if "attacks" in kwargs:
            kwargs["attacks"] = tuple(Data.attacks[a] for a in kwargs["attacks"])
        return cls(**kwargs)
