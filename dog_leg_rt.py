from typing import List

from color import Color
from shape import Shape

class DogLegRt(Shape):

    SHAPE: List[List[int]] = [[0, 1, 4, 8], [0, 4, 5, 6], [1, 5, 8, 9], [0, 1, 2, 6]]

    def __init__(self):
        super().__init__(self.SHAPE, Color.BLUE)

