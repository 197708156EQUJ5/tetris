from color import Color

class Tile():

    def __init__(self, color: Color = Color.BLACK, aid: int=0):
        self._color = color
        self._id = aid

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def get_id(self) -> int:
        return self._id

    def is_empty(self) -> bool:
        return self.color == Color.BLACK

