from dataclasses import dataclass
from TokenState import TokenState


@dataclass
class ContestResult:
    consume_attack: bool
    next_token: bool
    new_state: TokenState
