from shapes import Shape

class Piece():

     def __init__(self, shape: Shape, origin: tuple[int, int] = (3, 0), orientation: int = 0):
         self._shape = shape
         self._origin = origin
         self._orientation = orientation

     @property
     def shape(self):
         return self._shape

     @property
     def origin(self):
         return self._origin

     @origin.setter
     def origin(self, value):
         self._origin = value

     @property
     def orientation(self):
         return self._orientation

     @orientation.setter    
     def orientation(self, value):
         self._orientation = value
