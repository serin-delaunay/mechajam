from bearlibterminal import terminal as blt
from time import sleep
from Token import Token
from TokenType import TokenState
from Combatant import Combatant
from AttackResolver import AttackResolver
import Data


class Game:
    def __init__(self):
        self.stop = True
        self.width = 80
        self.height = 50
        self.next_turn_left = True
        self.highlighted_left = 0
        self.highlighted_right = 0
        self.selections_left = []
        self.selections_right = []
        Data.load()
        self.left_player = Combatant([Token(Data.tokens["Fist"], TokenState.healthy) for _ in range(10)])
        self.right_player = Combatant([Token(Data.tokens["Fist"], TokenState.healthy) for _ in range(10)], ai=True)

    def run(self):
        blt.open()
        blt.set(f"window.size={self.width}x{self.height}")
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

    def draw(self):
        assert self.width % 2 == 0, "Window size not divisible by 2"
        blt.clear()
        self.left_player.active = self.next_turn_left
        self.right_player.active = not self.next_turn_left
        for i, line in enumerate(self.left_player.display_lines()):
            blt.puts(0, i + 2, line, width=self.width // 2, height=1, align=blt.TK_ALIGN_LEFT)
        attacks = self.left_player.get_attacks()
        for (i, a) in enumerate(attacks):
            blt.put(i * 2, 0, a.symbol)

        for i, line in enumerate(self.right_player.display_lines()):
            blt.puts(self.width // 2, i + 2, line, width=self.width // 2, height=1, align=blt.TK_ALIGN_RIGHT)
        attacks = self.right_player.get_attacks()
        for (i, a) in enumerate(attacks):
            blt.put(self.width - 1 - (i * 2), 0, a.symbol)
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
