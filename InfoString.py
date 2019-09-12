from dataclasses import dataclass
from typing import Tuple
import re


@dataclass(frozen=True)
class InfoString:
    source: str
    formatted: str
    refs: Tuple[Tuple[str, str], ...]

    @staticmethod
    def colourise(info_type, name):
        if info_type == 'Attack':
            colour = "red"
        elif info_type == 'Token':
            colour = "green"
        else:
            colour = "yellow"
        return f"[color={colour}]{name}[/color]"

    @classmethod
    def from_source(cls, source):
        p = r"\[([^\[\]]*):([^\[\]]*)\]"
        matches = tuple(set(re.findall(p, source)))

        def repl(match):
            return cls.colourise(match.group(1), match.group(2))

        formatted = re.sub(p, repl, source)
        return cls(source, formatted, matches)
