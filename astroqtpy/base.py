import abc
from dataclasses import dataclass

import matplotlib as mpl


@dataclass
class QuadPoint():
    """Quadtree point.

    A dataclass for storing a value at coordinates (x, y).
    
    Args:
        _x (float): x position.
        _y (float): y position.
        _value (float, optional): Point value. Defaults to -1.
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
    """Quadtree base node.

    A base class for all released types of astroQTpy quadtree nodes.
    
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

        Create the base quad tree node for astroQTpy.
        """
        
        super().__init__()
        
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.depth = depth
        
        self.node_value = -1.0
        self.node_points = []  # to store QuadPoint objects
        
        self.child_nw = None
        self.child_ne = None
        self.child_sw = None
        self.child_se = None
     
    
    @abc.abstractmethod
    def generate_node_value(self):
        """Abstract method to generate node value.

        """
        pass
    
    
    def _get_node_value(self):
        """Convenience function to grab node value.
        
        """
        if True:
            self.generate_node_value()
        return self.node_value
    
    
    def _is_split(self):
        """Convenience function to check if this node has split.
        
        """
        return self.child_nw is not None
    
    
    def _print_points(self):
        """Convenience function to print out each point in this node.
        
        """
        if self.is_split():
            self.child_nw.print_points()
            self.child_ne.print_points()
            self.child_sw.print_points()
            self.child_se.print_points()
            
        else:
            print(f"# Depth = {self.depth}, x = {self.x_min:.5f} - {self.x_max:.5f}, " 
                  f"y = {self.y_min:.5f} - {self.y_max:.5f}")
            
            for point in self.node_points:
                print(f"{point.x:.5f}\t{point.y:.5f}\t{point.stable}\t")
          
          
    def _print_node_value(self):
        """Convenience function to print the value of this node.
        
        """
        if self.is_split():
            self.child_nw.print_node_value()
            self.child_ne.print_node_value()
            self.child_sw.print_node_value()
            self.child_se.print_node_value()
            
        else:
            print(f"{self.depth}\t{self.x_min:.5f}\t{self.x_max:.5f}\t" 
                  f"{self.y_min:.5f}\t{self.y_max:.5f}\t{self.get_node_value():.3f}\t")
            
            
    @abc.abstractmethod
    def split_node(self):
        """Abstract method to split this node into 4 equal child nodes.
        
        """
        pass
    
    
    def draw_node(self, ax, cmap: str = 'cividis_r', **ax_kwargs):
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
        
        cm = mpl.cm.get_cmap(cmap)
        
        if not self.is_split():
            ax.plot([x1, x2, x2, x1, x1], [y2, y2, y1, y1, y2], **ax_kwargs)
            ax.fill_between([x1,x2], [y1,y1], [y2,y2], color=cm(self.get_node_value()), alpha=0.8)
            ax.text(x_mid, y_mid, int(100*self.get_node_value()),
                    horizontalalignment="center", verticalalignment="center", c="k", size=10)