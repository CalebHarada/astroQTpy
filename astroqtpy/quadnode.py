import numpy as np 
from matplotlib import axes, cm

class QuadNode():
    """Quadtree node.

    A class for astroQTpy quadtree nodes. Each node is defined by its given boundary limits
    and 'depth', and may contain up to any given number of quadtree points.
    
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
        # check user specified attributes
        if x_max < x_min:
            raise ValueError('x_max must be greater than x_min.')
        elif x_max == x_min:
            raise ValueError('x_max cannot equal x_min.')
        elif not np.isfinite(x_min) or not np.isfinite(x_max):
            raise ValueError('x limits must be finite.')
        else:
            self.x_min = x_min
            self.x_max = x_max
        
        if y_max < y_min:
            raise ValueError('y_max must be greater than y_min.')
        elif y_max == y_min:
            raise ValueError('y_max cannot equal y_min.')
        elif not np.isfinite(y_max) or not np.isfinite(y_min):
            raise ValueError('y limits must be finite.')
        else:
            self.y_min = y_min
            self.y_max = y_max
        
        if depth < 0:
            raise ValueError('depth cannot be negative.')
        elif not np.isfinite(depth):
            raise ValueError('depth must be finite.')
        else:
            self.depth = depth
        
        # define other attributes
        self.node_value = -np.inf
        self.node_points = []  # to store QuadPoint objects
        self.child_nw = None
        self.child_ne = None
        self.child_sw = None
        self.child_se = None
     
    
    def split_node(self) -> None:
        """Split node.

        Split this node into 4 equal 'child' nodes. Distribute any points
        contained within this node to its children.
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
    
    
    def _generate_node_value(self, statistic: str) -> None:
        """Generate node value.
        
        Calculate an aggragate value of all points contained within this node.
        
        Args:
            statistic (str): Statistic to compute for this node. Choose from ['mean', 'std', or 'median'].
        """
                
        if len(self.node_points) == 0:
            return
        
        node_point_values = [point.value for point in self.node_points]
        
        if statistic == 'mean':
            self.node_value = np.mean(node_point_values)
        elif statistic == 'std':
            self.node_value = np.std(node_point_values)
        elif statistic == 'median':
            self.node_value = np.median(node_point_values)
        else:
            raise ValueError(" Node statistic must be either 'mean', 'std', or 'median'. ")
    
    
    def get_node_value(self, statistic: str) -> float:
        """Get node value.
        
        Convenience function to grab this node's value.
        
        Args:
            statistic (str): Statistic to pass to '_generate_node_value'. Choose from ['mean', 'std', or 'median'].

        Returns:
            float: Node value.
        """
        if self.node_value == -np.inf:
            self._generate_node_value(statistic)
            
        return self.node_value
    
    
    def _is_split(self) -> None:
        """Is split.
        
        Convenience function to check whether this node has been split.
        """
        return self.child_nw is not None
    
    
    def print_node_points(self) -> None:
        """Print node points.
        
        Convenience function to print each point contained within this node to a given file.
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
          
          
    def print_node_value(self, statistic: str) -> None:
        """Print node value.
        
        Convenience function to print the value of this node to a given file.
        
        Args:
            statistic (str): Statistic to pass to 'get_node_value'. Choose from ['mean', 'std', or 'median'].
        """
        if self._is_split():
            self.child_nw.print_node_value(statistic)
            self.child_ne.print_node_value(statistic)
            self.child_sw.print_node_value(statistic)
            self.child_se.print_node_value(statistic)
            
        else:
            print(f"{self.depth}\t{self.x_min:.5f}\t{self.x_max:.5f}\t" 
                  f"{self.y_min:.5f}\t{self.y_max:.5f}\t{self.get_node_value(statistic):.3f}\t")
    
    
    def draw_node(self, ax: axes.Axes, mappable: cm.ScalarMappable,
                  show_lines: bool, show_points: bool, show_values: bool,
                  statistic: str) -> None:
        """Draw node.

        Plot this node on a matplotlib axis.

        Args:
            ax (:obj:`matplotlib.axes.Axes`): Axis for plotting.
            mappable (:obj:`matplotlib.cm.ScalarMappable`): Scalar mappable for color mapping.
            show_lines (bool): Whether to draw boundary lines between nodes.
            show_points (bool): Whether to plot points contained within this node.
            show_values (bool): Whether to print the value of this node on the plot.
            statistic (str): Statistic to pass to 'get_node_value'. Choose from ['mean', 'std', or 'median'].
        """
        # grab node limits for convenience        
        x1, x2 = self.x_min, self.x_max
        y1, y2 = self.y_min, self.y_max
        
        if not self._is_split():
            ax.fill_between([x1,x2], [y1,y1], [y2,y2], color=mappable.to_rgba(self.get_node_value(statistic)))
            
            if show_lines:
                ax.plot([x1, x2, x2, x1, x1], [y2, y2, y1, y1, y2],
                        c="k", lw=1, alpha=0.5
                        )
            
            if show_points:
                ax.scatter(*zip(*[(point.x, point.y) for point in self.node_points]),
                           c='k', s=1, marker='.', alpha=0.8, rasterized=True
                           )
                
            if show_values:
                x_mid = 0.5 * (x1 + x2)
                y_mid = 0.5 * (y1 + y2)
                ax.text(x_mid, y_mid, round(self.get_node_value(statistic), 2),
                        horizontalalignment="center", verticalalignment="center", c="k", size=10
                        )