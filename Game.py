from bearlibterminal import terminal as blt
from time import sleep
from Token import Token, HealthToken, TokenState
from Attack import HitAttack


class Game:
    def __init__(self):
        self.health_points_left = [Token(HealthToken, TokenState.healthy) for _ in range(10)]
        self.health_points_right = [Token(HealthToken, TokenState.healthy) for _ in range(10)]
        self.stop = True
        self.width = 80
        self.height = 50
        self.next_turn_left = True

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
            attacker = self.health_points_left
            defender = self.health_points_right
        else:
            attacker = self.health_points_right
            defender = self.health_points_left

        attacks = self.get_attacks(attacker)

        self.resolve_combat(attacks, defender)

        self.next_turn_left = not self.next_turn_left

    @staticmethod
    def get_attacks(tokens):
        return [t for t in (token.attack() for token in tokens) if t is not None]

    @staticmethod
    def resolve_combat(attacks, defender):
        for attack in attacks:
            if attack is HitAttack:
                for token in defender:
                    if token.state is TokenState.healthy:
                        token.state = TokenState.damaged
                        break

    def draw(self):
        assert self.width % 2 == 0, "Window size not divisible by 2"
        blt.clear()
        for i, t in enumerate(self.health_points_left):
            blt.puts(0, i + 2, str(t), width=self.width//2, height=1, align=blt.TK_ALIGN_LEFT)
        attacks = self.get_attacks(self.health_points_left)
        for (i, a) in enumerate(attacks):
            blt.put(i * 2, 0, a.symbol)

        for i, t in enumerate(self.health_points_right):
            blt.puts(self.width//2, i + 2, str(t), width=self.width//2, height=1, align=blt.TK_ALIGN_RIGHT)
        attacks = self.get_attacks(self.health_points_right)
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
