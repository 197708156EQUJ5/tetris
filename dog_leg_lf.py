from typing import List

from color import Color
from shape import Shape

class DogLegLf(Shape):

    SHAPE: List[List[int]] = [[0, 1, 5, 9], [0, 1, 2, 4], [0, 4, 8, 9], [2, 4, 5, 6]]

    def __init__(self):
        super().__init__(self.SHAPE, Color.ORANGE)

