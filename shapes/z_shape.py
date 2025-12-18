from typing import List

from color import Color
from .shape import Shape

class ZShape(Shape):

    SHAPE: List[List[int]] = [[0, 1, 5, 6], [1, 4, 5, 8], [0, 1, 5, 6], [1, 4, 5, 8]]

    def __init__(self):
        super().__init__(self.SHAPE, Color.RED)

