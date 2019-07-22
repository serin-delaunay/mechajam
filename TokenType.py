from dataclasses import dataclass, field
from TokenMode import TokenMode
from TokenState import TokenState


@dataclass
class TokenType:
    name: str
    healthy: TokenMode = field(default_factory=TokenMode)
    damaged: TokenMode = field(default_factory=TokenMode)
    
    def mode(self, state: TokenState):
        if state is TokenState.healthy:
            return self.healthy
        elif state is TokenState.damaged:
            return self.damaged
        else:
            raise RuntimeError("Invalid token state")
    
    @classmethod
    def from_json(cls, **kwargs):
        if "healthy" in kwargs:
            kwargs["healthy"] = TokenMode.from_json(**kwargs["healthy"])
        if "damaged" in kwargs:
            kwargs["damaged"] = TokenMode.from_json(**kwargs["damaged"])
        return cls(**kwargs)

