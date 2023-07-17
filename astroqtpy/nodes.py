from .base_node import QuadNode

class NbodyNode(QuadNode):
    """Quadtree node for Nbody simulations.

    A node class for N-body simulations, inherits from the base class QuadNode.
    
    Args:
        x_min (float): Minimum x value of this node.
        x_max (float): Maximum x value of this node.
        y_min (float): Minimum y value of this node.
        y_max (float): Maximum y value of this node.
        depth (int, optional): Depth of this node. Defaults to 0.
    """
    
    def __init__(self, x_min, x_max, y_min, y_max, depth=0):
        """__init__

        Create the N-body quad tree node for astroQTpy.
        """
        super().__init__(x_min, x_max, y_min, y_max, depth)
        
        
    def generate_node_value(self):
        pass
    
    def split_node(self):
        pass