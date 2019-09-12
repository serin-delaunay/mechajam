from dataclasses import dataclass, field
from TokenMode import TokenMode
from TokenState import TokenState
from InfoString import InfoString
import Info


@dataclass
class TokenType:
    name: str
    healthy: TokenMode = field(default_factory=TokenMode)
    damaged: TokenMode = field(default_factory=TokenMode)
    info: str = ""
    
    def mode(self, state: TokenState):
        if state is TokenState.healthy:
            return self.healthy
        elif state is TokenState.damaged:
            return self.damaged
        else:
            raise RuntimeError("Invalid token state")
    
    @classmethod
    def from_json(cls, **kwargs):
        if "refs" in kwargs:
            kwargs["refs"] = tuple(kwargs["refs"])
        if "healthy" in kwargs:
            kwargs["healthy"] = TokenMode.from_json(**kwargs["healthy"])
        if "damaged" in kwargs:
            kwargs["damaged"] = TokenMode.from_json(**kwargs["damaged"])
        if "info" in kwargs:
            Info.info[("Token", kwargs["name"])] = InfoString.from_source(kwargs["info"])
        return cls(**kwargs)

