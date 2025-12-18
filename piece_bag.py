import random

from shapes import Shape, IShape, JShape, LShape, OShape, SShape, TShape, ZShape

class PieceBag:
    def __init__(self):
        self.bag = []
        self._refill()

    def _refill(self):
        self.bag = [IShape(), JShape(), LShape(), OShape(), SShape(), TShape(), ZShape()]
        random.shuffle(self.bag)

    def next(self) -> Shape:
        if len(self.bag) == 0:
            self._refill()
        return self.bag.pop(0)

    def peek(self) -> Shape:
        if len(self.bag) == 0:
            self._refill()
        return self.bag[0]

    def __str__(self):
        printstr = []
        for shape in self.bag:
            printstr.append(f"{shape}")

        printstr.append(f" {len(self.bag)}")

        return str(printstr)

