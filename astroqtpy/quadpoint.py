from dataclasses import dataclass
import numpy as np

@dataclass
class QuadPoint():
    """Quadtree point.

    A dataclass for storing a point value at coordinates (x, y).
    
    Args:
        _x (float): x position.
        _y (float): y position.
        _value (float, optional): Point value. Defaults to -inf.
    """
    _x: float
    _y: float
    _value: float = -np.inf
    
    @property
    def x(self) -> float:
        return self._x
    @x.setter
    def x(self, val: float) -> None:
        self._x = val
        
    @property
    def y(self) -> float:
        return self._y
    @y.setter
    def y(self, val: float) -> None:
        self._y = val
        
    @property
    def value(self) -> float:
        return self._value
    @value.setter
    def value(self, val: float) -> None:
        self._value = val