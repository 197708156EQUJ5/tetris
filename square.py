from typing import List

from color import Color
from shape import Shape

class Square(Shape):

    SHAPE: List[List[int]] = [[0, 1, 4, 5], [0, 1, 4, 5], [0, 1, 4, 5], [0, 1, 4, 5]]

    def __init__(self):
        super().__init__(self.SHAPE, Color.RED)

