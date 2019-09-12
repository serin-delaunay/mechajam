from dataclasses import dataclass, field
from typing import Tuple
import Info
from InfoString import InfoString

@dataclass
class Attack:
    name: str
    symbol: str
    info: str = ""
    refs: Tuple[str] = field(default_factory=tuple)

    @classmethod
    def from_json(cls, **kwargs):
        if "refs" in kwargs:
            kwargs["refs"] = tuple(kwargs["refs"])
        if "info" in kwargs:
            Info.info[("Attack", kwargs["name"])] = InfoString.from_source(kwargs["info"])
        return cls(**kwargs)

    def print_info(self):
        heading = f"[color=blue]{self.name}[/color]"
        body = f""
