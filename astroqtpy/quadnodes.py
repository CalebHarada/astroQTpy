import numpy as np

from .base import QuadNode

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

        Create the N-body quadtree node for astroQTpy.
        """
        super().__init__(x_min, x_max, y_min, y_max, depth)
    
    
    def split_node(self):
        """_summary_

        _extended_summary_
        """
        x_center = 0.5 * (self.x_min + self.x_max)
        y_center = 0.5 * (self.y_min + self.y_max)
        
        # create children
        self.child_nw = NbodyNode(self.x_min, x_center, y_center, self.y_max, self.depth + 1)
        self.child_ne = NbodyNode(x_center, self.x_max, y_center, self.y_max, self.depth + 1)
        self.child_sw = NbodyNode(self.x_min, x_center, self.y_min, y_center, self.depth + 1)
        self.child_se = NbodyNode(x_center, self.x_max, self.y_min, y_center, self.depth + 1)
        
        # distribute completed trials from parent node to child nodes
        for parent_point in self.node_points:
            # NW child
            if self.child_nw.x_min < parent_point.x < self.child_nw.x_max and \
               self.child_nw.y_min < parent_point.y < self.child_nw.y_max:
                self.child_nw.node_points.append(parent_point)
            
            # NE child
            if self.child_ne.x_min < parent_point.x < self.child_ne.x_max and \
               self.child_ne.y_min < parent_point.y < self.child_ne.y_max:
                self.child_ne.node_points.append(parent_point)
                
            # SW child
            if self.child_sw.x_min < parent_point.x < self.child_sw.x_max and \
               self.child_sw.y_min < parent_point.y < self.child_sw.y_max:
                self.child_sw.node_points.append(parent_point)
                
            # SE child
            if self.child_se.x_min < parent_point.x < self.child_se.x_max and \
               self.child_se.y_min < parent_point.y < self.child_se.y_max:
                self.child_se.node_points.append(parent_point)
        
        # clear parent node points
        self.node_points.clear()
        
        
