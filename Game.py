from bearlibterminal import terminal as blt
from time import sleep
from Token import Token, HealthToken, TokenState


class Game:
    def __init__(self):
        self.health_points_left = [Token(HealthToken, TokenState.healthy) for _ in range(10)]
        self.health_points_right = [Token(HealthToken, TokenState.healthy) for _ in range(10)]
        self.stop = True
        self.width = 80
        self.height = 50

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
        pass
        # fight

    def draw(self):
        assert self.width % 2 == 0, "Window size not divisible by 2"
        blt.clear()
        for i, s in enumerate(self.health_points_left):
            blt.puts(0, i + 2, s.type.name, width=self.width//2, height=1, align=blt.TK_ALIGN_LEFT)
            blt.put(i * 2, 0, s.attack().symbol)

        for i, s in enumerate(self.health_points_right):
            blt.puts(self.width//2, i + 2, s.type.name, width=self.width//2, height=1, align=blt.TK_ALIGN_RIGHT)
            blt.put(self.width - 1 - (i * 2), 0, s.attack().symbol)
        blt.refresh()

    def read(self):
        while blt.has_input():
            kp = blt.read()
            if kp == blt.TK_CLOSE:
                self.stop = True
            elif kp == blt.TK_SPACE:
                self.step()
