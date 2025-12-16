from typing import List

from color import Color
from shape import Shape

class IBeam(Shape):

    SHAPE: List[List[int]] = [[0, 4, 8, 12], [0, 1, 2, 3], [0, 4, 8, 12], [0, 1, 2, 3]]

    def __init__(self):
        super().__init__(self.SHAPE, Color.LT_BLUE)

