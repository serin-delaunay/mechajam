from bearlibterminal import terminal as blt
from time import sleep
from Token import Token
from TokenType import TokenState
from Combatant import Combatant
from AttackResolver import AttackResolver
from random import choice
import Data


class Game:
    def __init__(self):
        self.stop = True
        self.width = 80
        self.height = 50
        Data.load()
        self.left_player = None
        self.right_player = None
        self.next_turn_left = True

    def new_game(self):
        self.left_player = self.generate_combatant(ai=True)
        self.right_player = self.generate_combatant(ai=True)
        self.next_turn_left = True

    @staticmethod
    def generate_combatant(ai=False):
        tokens = []
        for i in range(10):
            tokens.append(Token(choice(list(Data.tokens.values())), TokenState.healthy))
        for i in range(2):
            tokens.append(Token(Data.tokens["Heart"], TokenState.healthy))
        return Combatant(tokens, ai=ai)

    def run(self):
        blt.open()
        blt.set(f"window.size={self.width}x{self.height}")
        self.new_game()
        self.stop = False
        while not self.stop:
            self.draw()
            sleep(0.01)
            self.read()
        pass

    def step(self):
        self.active_player().process_activations()
        ar = AttackResolver(self.active_player(), self.inactive_player())
        ar.resolve_combat()
        self.next_turn_left = not self.next_turn_left
        if self.active_player().ai:
            self.active_player().automate_activations()

    def active_player(self):
        return self.left_player if self.next_turn_left else self.right_player

    def inactive_player(self):
        return self.right_player if self.next_turn_left else self.left_player
        
    def draw_tokens(self, player, align_right=False):
        left = self.width // 2 if align_right else 0
        align = blt.TK_ALIGN_RIGHT if align_right else blt.TK_ALIGN_LEFT
        for i, line in enumerate(player.display_lines()):
            blt.puts(left, i + 2, line, width=self.width // 2, height=1, align=align)
            
    def draw_attacks(self, player, align_right=False):
        for (i, a) in enumerate(player.get_attacks()):
            x = self.width - 1 - (i * 2) if align_right else (i * 2)
            blt.put(x, 0, a.symbol)
        
    def draw(self):
        assert self.width % 2 == 0, "Window size not divisible by 2"
        blt.clear()
        self.left_player.active = self.next_turn_left
        self.right_player.active = not self.next_turn_left
        
        self.draw_tokens(self.left_player)
        self.draw_attacks(self.left_player)
        self.draw_tokens(self.right_player, True)
        self.draw_attacks(self.right_player, True)

        blt.refresh()

    def read(self):
        while blt.has_input():
            kp = blt.read()
            if kp == blt.TK_CLOSE:
                self.stop = True
            elif kp == blt.TK_SPACE:
                self.step()
            elif kp == blt.TK_UP:
                self.active_player().move_up()
            elif kp == blt.TK_DOWN:
                self.active_player().move_down()
            elif kp == blt.TK_LEFT:
                self.active_player().move_left()
            elif kp == blt.TK_RIGHT:
                self.active_player().move_right()
            elif kp == blt.TK_R:
                self.new_game()
