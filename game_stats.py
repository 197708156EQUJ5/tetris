class GameStats():

    BASE_POINTS = {
        1: 40,
        2: 100,
        3: 300,
        4: 1200
    }

    def __init__(self):
        self._level: int = 0
        self._lines_cleared: int = 9
        self._score: int = 0

    def on_lines_cleared(self, count: int=1):
        if count not in self.BASE_POINTS:
            return

        self._score += self.BASE_POINTS[count] * (self._level + 1)
        self._lines_cleared += count
        self._level = self._lines_cleared // 10

    @property
    def level(self):
        return self._level

    @property
    def lines_cleared(self):
        return self._lines_cleared

    @property
    def score(self):
        return self._score

