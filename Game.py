from bearlibterminal import terminal as blt
from time import sleep


class Game:
    def __init__(self):
        self.health_points = ['Health' for _ in range(10)]
        self.stop = True

    def run(self):
        blt.open()
        self.stop = False
        while not self.stop:
            self.draw()
            sleep(0.01)
            self.read()
        pass

    def draw(self):
        blt.clear()
        for i, s in enumerate(self.health_points):
            blt.printf(0, i, s)
        blt.refresh()

    def read(self):
        while blt.has_input():
            if blt.read() == blt.TK_CLOSE:
                self.stop = True
