from bearlibterminal import terminal as blt
from time import sleep
from Token import Token, HealthToken, TokenState
from Attack import HitAttack
from Combatant import Combatant


class Game:
    def __init__(self):
        self.left_player = Combatant([Token(HealthToken, TokenState.healthy) for _ in range(10)])
        self.right_player = Combatant([Token(HealthToken, TokenState.healthy) for _ in range(10)])
        self.stop = True
        self.width = 80
        self.height = 50
        self.next_turn_left = True
        self.highlighted_left = 0
        self.highlighted_right = 0
        self.selections_left = []
        self.selections_right = []

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
        if self.next_turn_left:
            self.resolve_combat(self.left_player, self.right_player)
        else:
            self.resolve_combat(self.right_player, self.left_player)
        self.next_turn_left = not self.next_turn_left

    @staticmethod
    def resolve_combat(attacker, defender):
        attacks = attacker.get_attacks()
        for attack in attacks:
            if attack is HitAttack:
                for token in defender.health_tokens:
                    if token.state is TokenState.healthy:
                        token.state = TokenState.damaged
                        break

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
