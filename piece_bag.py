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
        if len(self.bag) < 2:
            self._refill()
        return self.bag.pop(0)

    def peek(self) -> Shape:
        return self.bag[0]
