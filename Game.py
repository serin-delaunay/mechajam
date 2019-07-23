from bearlibterminal import terminal as blt
from time import sleep
from Token import Token
from TokenType import TokenState
from Combatant import Combatant
from ContestResult import ContestResult
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
        self.resolve_combat(self.active_player(), self.inactive_player())
        self.next_turn_left = not self.next_turn_left
        if self.active_player().ai:
            self.active_player().automate_activations()

    def active_player(self):
        return self.left_player if self.next_turn_left else self.right_player

    def inactive_player(self):
        return self.right_player if self.next_turn_left else self.left_player

    @staticmethod
    def resolve_contest(attack, token):
        if token.state is TokenState.damaged:
            return ContestResult(False, True, TokenState.damaged)
        else:
            return ContestResult(True, True, TokenState.damaged)

    @classmethod
    def resolve_combat(cls, attacker, defender):
        attacks = attacker.get_attacks()
        attack_index = 0
        token_index = 0
        stop = len(attacks) == 0

        while not stop:
            attack = attacks[attack_index]
            token = defender.health_tokens[token_index]
            result = cls.resolve_contest(attack, token)
            token.state = result.new_state
            if result.consume_attack:
                if attack_index < len(attacks) - 1:
                    attack_index += 1
                else:
                    stop = True
            if result.next_token:
                if token_index < len(defender.health_tokens) - 1:
                    token_index += 1
                else:
                    stop = True

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
