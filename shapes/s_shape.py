from typing import List

from color import Color
from .shape import Shape

class SShape(Shape):

    SHAPE: List[List[int]] = [[1, 2, 4, 5], [0, 4, 5, 9], [1, 2, 4, 5], [0, 4, 5, 9]]

    def __init__(self):
        super().__init__(self.SHAPE, Color.GREEN)

