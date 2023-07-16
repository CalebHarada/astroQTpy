import abc
from dataclasses import dataclass

@dataclass
class QuadPoint():
    """Quadtree point

    A data class to store a value at coordinates (x, y).
    """
    _x : float
    _y : float
    _value : float = -1
    
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



class QuadNode(abc.ABC):
    """Quadtree node

    An abstract class for a quadtree node.

    Args:
        
    """
    def __init__(self) -> None:
        super().__init__()
        
        