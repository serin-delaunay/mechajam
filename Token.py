from dataclasses import dataclass
from TokenType import TokenType
from TokenState import TokenState


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

    def mode(self):
        return self.type.mode(self.state)

    def attack(self):
        return self.mode().attacks

    def display(self, highlighted: bool, selected: bool):
        fg, bg = self.fg_bg_colours(highlighted, selected)
        return f"[color={fg}][bkcolor={bg}]{self.type.name}[/bkcolor][/color]"
