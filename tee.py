from typing import List

from color import Color
from shape import Shape

class Tee(Shape):

    SHAPE: List[List[int]] = [[1, 4, 5, 6], [1, 4, 5, 9], [0, 1, 2, 5], [1, 5, 6, 9]]

    def __init__(self):
        super().__init__(self.SHAPE, Color.PURPLE)

