import random

from dog_leg_lf import DogLegLf
from dog_leg_rt import DogLegRt
from ess import Ess
from i_beam import IBeam
from shape import Shape
from square import Square
from tee import Tee
from zee import Zee

class PieceBag:
    def __init__(self):
        self.bag = []
        self._refill()

    def _refill(self):
        self.bag = [DogLegRt(), DogLegLf(), Square(), Zee(), Tee(), Ess(), IBeam()]
        random.shuffle(self.bag)

    def next(self) -> Shape:
        if len(self.bag) < 2:
            self._refill()
        return self.bag.pop(0)

    def peek(self) -> Shape:
        return self.bag[0]
