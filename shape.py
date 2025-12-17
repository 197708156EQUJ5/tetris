from typing import List

from color import Color
from heading import Heading

class Shape():

    def __init__(self, shape_lists: List[List[int]], color: Color=Color.BLACK):
        self.shape_lists = shape_lists
        self._color = color
    
    def get_shape(self, orientation) -> List[int]:
        return self.shape_lists[orientation]

    @property
    def color(self) -> Color:
        return self._color

    def __str__(self):
        return f"{self.__class__.__name__}"

