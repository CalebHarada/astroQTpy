import numpy as np 
import matplotlib as mpl 

class QuadNode():
    """Quadtree node.

    A class for astroQTpy quadtree nodes.
    
    Args:
        x_min (float): Minimum x value of this node.
        x_max (float): Maximum x value of this node.
        y_min (float): Minimum y value of this node.
        y_max (float): Maximum y value of this node.
        depth (int, optional): Depth of this node. Defaults to 0.
    """
    def __init__(self,
        x_min : float,
        x_max : float,
        y_min : float,
        y_max : float,
        depth : int = 0
        ) -> None:
        """__init__

        Create a quadtree node for astroQTpy.
        """        
        # from args
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.depth = depth
        
        # define attributes
        self.node_value = -np.inf
        self.node_points = []  # to store QuadPoint objects
        self.child_nw = None
        self.child_ne = None
        self.child_sw = None
        self.child_se = None
     
    
    def split_node(self) -> None:
        """Split node.

        Split this node into 4 equal child nodes and distribute parent node points to children.
        """
        x_center = 0.5 * (self.x_min + self.x_max)
        y_center = 0.5 * (self.y_min + self.y_max)
        
        # create children
        self.child_nw = QuadNode(self.x_min, x_center, y_center, self.y_max, self.depth + 1)
        self.child_ne = QuadNode(x_center, self.x_max, y_center, self.y_max, self.depth + 1)
        self.child_sw = QuadNode(self.x_min, x_center, self.y_min, y_center, self.depth + 1)
        self.child_se = QuadNode(x_center, self.x_max, self.y_min, y_center, self.depth + 1)
        
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
    
    
    def _generate_node_value(self, statistic: str = 'mean') -> None:
        """Generate node value.
        
        Args:
            statistic (str, optional): Statistic to compute for this node. Defaults to 'mean'.
        """
        
        # TO DO: allow multiple options for statistic (e.g., std, median, mean...)
        
        if len(self.node_points) == 0:
            return
        
        node_point_values = [point.value for point in self.node_points]
        
        if statistic == 'mean':
            self.node_value = np.mean(node_point_values)
    
    
    def get_node_value(self):
        """Convenience function to grab node value.
        
        """
        if self.node_value == -np.inf:
            self._generate_node_value()
            
        return self.node_value
    
    
    def _is_split(self):
        """Convenience function to check if this node has split.
        
        """
        return self.child_nw is not None
    
    
    def print_node_points(self):
        """Convenience function to print out each point in this node.
        
        """
        if self._is_split():
            self.child_nw.print_node_points()
            self.child_ne.print_node_points()
            self.child_sw.print_node_points()
            self.child_se.print_node_points()
            
        else:
            print(f"# Depth = {self.depth}, x = {self.x_min:.5f} - {self.x_max:.5f}, " 
                  f"y = {self.y_min:.5f} - {self.y_max:.5f}")
            
            for point in self.node_points:
                print(f"{point.x:.5f}\t{point.y:.5f}\t{point.value}\t")
          
          
    def print_node_value(self):
        """Convenience function to print the value of this node.
        
        """
        if self._is_split():
            self.child_nw.print_node_value()
            self.child_ne.print_node_value()
            self.child_sw.print_node_value()
            self.child_se.print_node_value()
            
        else:
            print(f"{self.depth}\t{self.x_min:.5f}\t{self.x_max:.5f}\t" 
                  f"{self.y_min:.5f}\t{self.y_max:.5f}\t{self.get_node_value():.3f}\t")
    
    
    def draw_node(self, ax, mappable, show_points, show_values, **ax_kwargs) -> None:
        """Draw node

        Plot this node on a matplotlib axis.

        Args:
            ax (:obj:`matplotlib.pyplot.Axes`): Axis for plotting.
            cmap (str, optional): Matplotlib colormap for nodes. Defaults to 'cividis_r'.
            **ax_kwargs: Keyword arguments passed to :obj:`matplotlib.pyplot.Axes` object.
        """
        
        # TO DO: make plotting more customizable
        
        x1, x2 = self.x_min, self.x_max
        y1, y2 = self.y_min, self.y_max
        x_mid = 0.5 * (x1 + x2)
        y_mid = 0.5 * (y1 + y2)
        
        if not self._is_split():
            ax.plot([x1, x2, x2, x1, x1], [y2, y2, y1, y1, y2], c="k", lw=1, alpha=0.5, **ax_kwargs)
            ax.fill_between([x1,x2], [y1,y1], [y2,y2], color=mappable.to_rgba(self.get_node_value()))
            
            if show_points:
                ax.scatter(*zip(*[(point.x, point.y) for point in self.node_points]),
                           c='k', s=1, marker='.', alpha=0.5, rasterized=True
                           )
                
            if show_values:
                ax.text(x_mid, y_mid, round(self.get_node_value(), 2),
                        horizontalalignment="center", verticalalignment="center", c="k", size=10)