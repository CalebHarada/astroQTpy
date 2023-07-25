import sys
import abc

import numpy as np
from matplotlib import axes, cm, colors
from rebound.interruptible_pool import InterruptiblePool  # import throws `pkg_resources.declare_namespace` warning

from .quadnode import QuadNode
from .quadpoint import QuadPoint


class BaseTree(abc.ABC):
    """Base quadtree.

    The abstract base class for all types of astroQTpy quadtrees.

    Args:
        x_min (float): Minimum x value for this quadtree.
        x_max (float): Maximum x value for this quadtree.
        y_min (float): Minimum y value for this quadtree.
        y_max (float): Maximum y value for this quadtree.
        split_threshold (float, optional): Threshold discrepancy in order to split nodes. Defaults to 0.2.
        node_statistic (str, optional): Statistic to compute node values ['mean', 'std', or 'median']. Defaults to 'mean'.
        N_points (int, optional): Maximum number of points per node. Defaults to 20.
        min_depth (int, optional): Minimum quadtree depth. Defaults to 3.
        max_depth (int, optional):  Maximum quadtree depth. Defaults to 6.
        N_proc (int, optional): Number of cores for multiprocessing. Defaults to 1.
        verbose (bool, optional): Option to print node values in real time. Defaults to False.
        filename_points (str, optional): Name of output file to save points. Defaults to 'points.txt'.
        filename_nodes (str, optional): Name of output file to save nodes. Defaults to 'nodes.txt'.
    """

    def __init__(self,
        x_min: float,
        x_max: float,
        y_min: float,
        y_max: float,
        split_threshold: float = 0.2,
        node_statistic: str = 'mean',
        N_points: int = 20,
        min_depth: int = 3,
        max_depth: int = 6,
        N_proc: int = 1,
        verbose: bool = False,
        filename_points: str = 'points.txt',
        filename_nodes: str = 'nodes.txt'
        ) -> None:
        """__init__

        Create the base quadtree class for astroQTpy.
        """
        
        super().__init__()
        
        # check user input attributes
        if split_threshold <= 0:
            raise ValueError('split_threshold must be greater than zero.')
        elif not np.isfinite(split_threshold):
            raise ValueError('split_threshold must be finite.')
        else:
            self.split_threshold = split_threshold
            
        if node_statistic in ['mean', 'median', 'std']:
            self.node_statistic = node_statistic
        else:
            raise ValueError('node_statistic must be either "mean, "median", or "std"')
        
        if N_points <= 0:
            raise ValueError('N_points must be greater than zero.')
        else:
            self.N_points = N_points
            
        if max_depth < min_depth:
            raise ValueError('max_depth must be greater than min_depth.')
        else:
            self.min_depth = min_depth
            self.max_depth = max_depth
            
        if N_proc <= 0:
            raise ValueError('N_proc must be greater than zero.')
        else:
            self.N_proc = N_proc
        
        # define other attributes
        self.verbose = verbose
        self.filename_points = filename_points
        self.filename_nodes = filename_nodes
        self.node_count = 1
        self.root = QuadNode(x_min, x_max, y_min, y_max, 1)
        self.min_node_value = np.inf  # for plotting limits
        self.max_node_value = -np.inf
        
    
    def _compare_nodes(self, northwest: QuadNode, southeast: QuadNode, dir_northsouth: bool = False) -> None:
        """Compare nodes.

        Compare values of two nodes and split into 4 children if threshold is exceeded.

        Args:
            northwest (QuadNode): First quadtree node.
            southeast (QuadNode): Second quadtree node.
            dir_northsouth (bool, optional): Whether the nodes being compared are aligned N-S. Defaults to False.
        """
        
        # if both northwest and southeast nodes are split
        if northwest._is_split() and southeast._is_split():
            if dir_northsouth:
                self._compare_nodes(northwest.child_sw, southeast.child_nw, True)
                self._compare_nodes(northwest.child_se, southeast.child_ne, True)
            else:
                self._compare_nodes(northwest.child_ne, southeast.child_nw, False)
                self._compare_nodes(northwest.child_se, southeast.child_sw, False)
                
        # if northwest is split and southeast is NOT split
        elif northwest._is_split() and not southeast._is_split():
            if dir_northsouth:
                self._compare_nodes(northwest.child_sw, southeast, True)
                self._compare_nodes(northwest.child_se, southeast, True)
            else:
                self._compare_nodes(northwest.child_ne, southeast, False)
                self._compare_nodes(northwest.child_se, southeast, False)
            
        # if northwest is NOT split and southeast is split
        elif not northwest._is_split() and southeast._is_split():
            if dir_northsouth:
                self._compare_nodes(northwest, southeast.child_nw, True)
                self._compare_nodes(northwest, southeast.child_ne, True)
            else:
                self._compare_nodes(northwest, southeast.child_nw, False)
                self._compare_nodes(northwest, southeast.child_sw, False)
                
        # if neither node is split
        else:
            if abs(northwest.get_node_value(self.node_statistic) - southeast.get_node_value(self.node_statistic)) >= self.split_threshold:
                if northwest.depth >= southeast.depth and southeast.depth < self.max_depth:
                    southeast.split_node()
                    self.fill(southeast, self.N_points)
                    self._save_checkpoint()
                    
                if southeast.depth >= northwest.depth and northwest.depth < self.max_depth:
                    northwest.split_node()
                    self.fill(northwest, self.N_points)
                    self._save_checkpoint()
                    
                    
    def fill(self, node: QuadNode, N_points: int) -> None:
        """Fill.

        Fill a given node with points.

        Args:
            node (QuadNode): The quadtree node to be filled.
            N_points (int): Number of points to put inside this node.
        """
        if node._is_split():
            self.fill(node.child_nw, N_points)
            self.fill(node.child_ne, N_points)
            self.fill(node.child_sw, N_points)
            self.fill(node.child_se, N_points)
            return
        
        if self.N_proc > 1:
            self.evaluate_multiple_points(node, N_points)

        else:
            while len(node.node_points) < N_points:
                point = self.evaluate_point(node, rng_seed=np.random.randint(1, 1e8))
                node.node_points.append(point)
     
     
    def evaluate_multiple_points(self, node: QuadNode, N_points: int) -> None:
        """Evaulate multiple points.

        Evaluate multiple points contained within a given node in parallel.

        Args:
            node (QuadNode): Node in which to evaulate points.
            N_points (int): Maximum number of points to evaulate within this node.
        """
        N_empty = int(N_points - len(node.node_points))
        map_iters = [(node, np.random.randint(1, 1e8)) for _ in range(N_empty)]
        
        with InterruptiblePool(processes=self.N_proc) as pool:
            points = pool.starmap(self.evaluate_point, map_iters)
            for point in points:
                node.node_points.append(point)
                
                
    @abc.abstractmethod
    def evaluate_point(self, node: QuadNode, rng_seed: int = 123456) -> QuadPoint:
        """Evaluate point.

        Abstract method to calculate the value of one point within a given node.

        Args:
            node (QuadNode): Node in which to evaulate point.
            rng_seed (int, optional): Random number generator seed. Defaults to 123456.

        Returns:
            QuadPoint: A QuadPoint object that has been evaluated.
        """
        pass
    
    
    def _save_checkpoint(self) -> None:
        """Save checkpoint.
        
        Convenience function to save progress and update node count (called any time a node is split).
        """
        self.node_count = self.node_count + 3
        self.print_all_points()
        self.print_all_nodes()
        if self.verbose:
            print(f"Progress saved. (nodes = {self.node_count})")
        
    
    def print_all_points(self) -> None:
        """Print all points.
        
        Print all current quadtree points to a file ('filename_points').
        """
        stdout_ = sys.stdout
        f = open(self.filename_points, 'w')
        sys.stdout = f
        
        print("# x \t y \t value")
        self.root.print_node_points()
        sys.stdout = stdout_
        
        f.close()
        
    
    def print_all_nodes(self) -> None:
        """Print all nodes.
        
        Print all current quadtree node values to a file ('filename_nodes').
        """
        stdout_ = sys.stdout
        f = open(self.filename_nodes, 'w')
        sys.stdout = f
        
        print("# Depth \t x_min \t x_max \t y_min \t y_max \t node value")
        self.root.print_node_value(self.node_statistic)
        sys.stdout = stdout_
        
        f.close()
    
    
    def load_points(self) -> None:
        """Load points.
        
        Load all points from a previously saved quadtree.
        """
        with open(self.filename_points, 'r') as f:
            for line in f:
                if line[0] == "#":
                    continue
                line_spl = line.split('\t')
                point = QuadPoint(float(line_spl[0]), float(line_spl[1]), float(line_spl[2]))
                self.root.node_points.append(point)
        
        self.squeeze_node(self.root)
        
    
    def squeeze_node(self, node: QuadNode) -> None:
        """Squeeze node.
        
        Distribute quadtree points from parent to children.
        """
        if len(node.node_points) > self.N_points and node.depth < self.max_depth:
            node.split_node()
            self.node_count = self.node_count + 3
        
        if node._is_split():
            self.squeeze_node(node.child_nw)
            self.squeeze_node(node.child_ne)
            self.squeeze_node(node.child_sw)
            self.squeeze_node(node.child_se)
            
            
    def run_quadtree(self) -> None:
        """Run quadtree.
        
        Run the quadtree from a previously saved run, or start a new run.
        """
        # attempt to load previous results
        try:
            print("Attempting to load previous results...")
            self.load_points()
            print(f"   {self.node_count} nodes found, starting from previous checkpoint...")
        except FileNotFoundError:
            print("   No previous results found, starting new...")

        # must execute at least minimum depth nodes
        for _ in range(self.min_depth):
            self._forward(self.root)

        # save
        self._save_checkpoint()
        
        print("DONE! :)")
        
        
    def _forward(self, node: QuadNode) -> None:
        """Forward.
        
        Advance quadtree forward a step by comparing child nodes and expanding resolution where necessary.
        
        Args:
            node (QuadNode): Quadtree node.
        """
        if node._is_split():
            self._compare_nodes(node.child_nw, node.child_ne, False)
            self._compare_nodes(node.child_sw, node.child_se, False)
            self._compare_nodes(node.child_nw, node.child_sw, True)
            self._compare_nodes(node.child_ne, node.child_se, True)
        elif node.depth < self.min_depth:
            node.split_node()
            self._save_checkpoint()
            
        if node._is_split():
            self._forward(node.child_nw)
            self._forward(node.child_ne)
            self._forward(node.child_sw)
            self._forward(node.child_se)
        elif len(node.node_points) < self.N_points:
            if self.N_proc > 1:
                self.evaluate_multiple_points(node, self.N_points)
            else:
                while len(node.node_points) < self.N_points:
                    point = self.evaluate_point(node, rng_seed=np.random.randint(1, 1e8))
                    node.node_points.append(point)
                    
                    
    def _get_min_max_nodes(self, node: QuadNode) -> None:
        """Get min max nodes.

        Convenience function to grab the minimum and maximum node values for plotting.

        Args:
            node (QuadNode): Starting quadtree node.
        """
        if node._is_split():
            self._get_min_max_nodes(node.child_nw)
            self._get_min_max_nodes(node.child_ne)
            self._get_min_max_nodes(node.child_sw)
            self._get_min_max_nodes(node.child_se)
        
        if node.get_node_value(self.node_statistic) > self.max_node_value:
            self.max_node_value = node.get_node_value(self.node_statistic)
            
        if node.get_node_value(self.node_statistic) < self.min_node_value and node.get_node_value(self.node_statistic) != -np.inf:
            self.min_node_value = node.get_node_value(self.node_statistic)
                                
    
    def _draw_nodes(self, ax: axes.Axes, node: QuadNode, mappable: cm.ScalarMappable,
                    show_lines: bool, show_points: bool, show_values: bool) -> None:
        """Draw nodes.
        
        Convenience function to plot quadtree nodes, including children.
        
        Args:
            ax (:obj:`matplotlib.axes.Axes`): Axis for plotting.
            node (QuadNode): Quadtree node.
            mappable (:obj:`matplotlib.cm.ScalarMappable`): Scalar mappable for color mapping.
            show_lines (bool): Whether to draw boundary lines between nodes.
            show_points (bool): Whether to plot points contained within this node.
            show_values (bool): Whether to print the value of this node on the plot.
        """
        
        if node._is_split():
            self._draw_nodes(ax, node.child_nw, mappable, show_lines, show_points, show_values)
            self._draw_nodes(ax, node.child_ne, mappable, show_lines, show_points, show_values)
            self._draw_nodes(ax, node.child_sw, mappable, show_lines, show_points, show_values)
            self._draw_nodes(ax, node.child_se, mappable, show_lines, show_points, show_values)
            
        node.draw_node(ax, mappable, show_lines, show_points, show_values, self.node_statistic)
        
    
    def draw_tree(self, ax: axes.Axes,
                  cmap: str = 'RdYlGn_r',
                  vmin: float = None,
                  vmax: float = None,
                  show_lines: float = True,
                  show_points: bool = False,
                  show_values: bool = False
                  ) -> cm.ScalarMappable:
        """Draw quadtree. 
        
        Plot the entire quadtree on a given axis.

        Args:
            ax (:obj:`matplotlib.axes.Axes`): Matplotlib axis for plotting.
            cmap (str, optional): Matplotlib colormap. Defaults to 'RdYlGn_r'.
            vmin (float, optional): Minimum value for colorbar. Defaults to None.
            vmax (float, optional): Maximum value for colorbar. Defaults to None.
            show_lines (float, optional): Option to plot node boundary lines. Defaults to True.
            show_points (bool, optional): Option to plot node points. Defaults to False.
            show_values (bool, optional): Option to print node values on plot. Defaults to False.

        Returns:
            matplotlib.cm.ScalarMappable: Matplotlib ScalarMappable.
        """
        if vmin is None:
            self._get_min_max_nodes(self.root)
            vmin = 0.8 * self.min_node_value
        if vmax is None:
            self._get_min_max_nodes(self.root)
            vmax = 1.2 * self.max_node_value
        
        mappable = cm.ScalarMappable(
            colors.Normalize(vmin, vmax),
            cmap=cmap
            )
        
        self._draw_nodes(ax, self.root, mappable, show_lines, show_points, show_values)
        
        return mappable
