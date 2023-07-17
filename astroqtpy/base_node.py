import abc

class QuadNode(abc.ABC):
    """Quadtree node

    An base class for all released types of astroQTpy quadtree nodes.
    """
    def __init__(self,
        x_min : float,
        x_max : float,
        y_min : float,
        y_max : float,
        depth : int = 0
        ) -> None:
        """__init__

        Create the base quad tree node for astroQTpy.

        Args:
            x_min (float): Minimum x value of this node
            x_max (float): Maximum x value of this node
            y_min (float): Minimum y value of this node
            y_max (float): Maximum y value of this node
            depth (int, optional): Depth of this node. Defaults to 0.
        """
        
        super().__init__()
        
        self._x_min = x_min
        self._x_max = x_max
        self._y_min = y_min
        self._y_max = y_max
        self._depth = depth
        
        self.node_value = -1.0
        self.node_points = []  # to store QuadPoint objects
        
    
    @abc.abstractmethod
    def generate_node_value(self):
        pass
    
    
        
        