import sys
import abc

import numpy as np
import matplotlib as mpl
from rebound.interruptible_pool import InterruptiblePool  # import throws `pkg_resources.declare_namespace` warning

from .quadnode import QuadNode
from .quadpoint import QuadPoint


# CH: I think you might want to make QuadNode just a regular class.
# QuadTree could be an ABC because the specific purpose of the
# tree is implemented there. Whereas for QuadNode, nothing really
# inherently changes between different uses -- it's just a class
# to contain and organize QuadPoints.


class BaseTree(abc.ABC):
    """Base quadtree class.

    A base quadtree class for all released types of astroQTpy quadtrees.
    
    Args:
        
    """
    def __init__(self,
        x_min: float,
        x_max: float,
        y_min: float,
        y_max: float,
        split_threshold: float = 0.2,
        N_points: int = 20,
        min_depth: int = 3,
        max_depth: int = 6,
        N_proc: int = 4,
        verbose: bool = True,
        filename_points: str = 'points.txt',
        filename_nodes: str = 'nodes.txt'
        ) -> None:
        """Initialization

        Create the base quadtree class for astroQTpy.
        """
        super().__init__()
        
        # from args
        self.split_threshold = split_threshold
        self.N_points = N_points
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.N_proc = N_proc
        self.verbose = verbose
        self.filename_points = filename_points
        self.filename_nodes = filename_nodes
        
        # define attributes
        self.node_count = 1
        self.root = QuadNode(x_min, x_max, y_min, y_max, 1)
        self.min_node_value = np.inf
        self.max_node_value = -np.inf
        
    
    def _compare_nodes(self, northwest: QuadNode, southeast: QuadNode, dir_northsouth: bool = False):
        """Compare two nodes and split into children if necessary.
        
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
            if abs(northwest.get_node_value() - southeast.get_node_value()) >= self.split_threshold:
                if northwest.depth >= southeast.depth and southeast.depth < self.max_depth:
                    southeast.split_node()
                    self.fill(southeast, self.N_points)
                    if self.verbose: self._save_checkpoint()
                    
                if southeast.depth >= northwest.depth and northwest.depth < self.max_depth:
                    northwest.split_node()
                    self.fill(northwest, self.N_points)
                    if self.verbose: self._save_checkpoint()
                    
                    
    def fill(self, node: QuadNode, N_points: int):
        """Fill the given node with points.
        
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
     
     
    def evaluate_multiple_points(self, node: QuadNode, N_points: int):
        """Evaluate multiple points within a node in parallel.
        
        """
        N_empty = int(N_points - len(node.node_points))
        map_iters = [(node, np.random.randint(1, 1e8)) for _ in range(N_empty)]
        
        with InterruptiblePool(processes=self.N_proc) as pool:
            points = pool.starmap(self.evaluate_point, map_iters)
            for point in points:
                node.node_points.append(point)
                
                
    @abc.abstractmethod
    def evaluate_point(self, node: QuadNode, rng_seed: int = 123456) -> QuadPoint:
        """Evaluate point

        Abstract method to calculate the value of one point within a given node.

        Args:
            node (QuadNode): _description_
            rng_seed (int, optional): _description_. Defaults to 123456.

        Returns:
            QuadPoint: _description_
        """
        pass
    
    
    def _save_checkpoint(self):
        """Convenience function to save progress and update node count
        (called any time a node is split).
        
        """
        self.node_count = self.node_count + 3
        self.print_all_points()
        self.print_all_nodes()
        print(f"Progress saved. (nodes = {self.node_count})")
        
    
    def print_all_points(self):
        """Print all current quadtree points to a file ('filename_points').
        
        """
        stdout_ = sys.stdout
        f = open(self.filename_points, 'w')
        sys.stdout = f
        
        print("# x \t y \t value")
        self.root.print_node_points()
        sys.stdout = stdout_
        
        f.close()
        
    
    def print_all_nodes(self):
        """Print all current quadtree nodes to a file ('filename_nodes').
        
        """
        stdout_ = sys.stdout
        f = open(self.filename_nodes, 'w')
        sys.stdout = f
        
        print("# Depth \t x_min \t x_max \t y_min \t y_max \t node value")
        self.root.print_node_value()
        sys.stdout = stdout_
        
        f.close()
    
    
    def load_points(self):
        """Load all points from a previously saved run.
        
        """
        with open(self.filename_points, 'r') as f:
            for line in f:
                if line[0] == "#":
                    continue
                line_spl = line.split('\t')
                point = QuadPoint(float(line_spl[0]), float(line_spl[1]), float(line_spl[2]))
                self.root.node_points.append(point)
        
        self.squeeze_node(self.root)
        
    
    def squeeze_node(self, node: QuadNode):
        """Distribute points to child nodes.
        
        """
        if len(node.node_points) > self.N_points and node.depth < self.max_depth:
            node.split_node()
            self.node_count = self.node_count + 3
        
        if node._is_split():
            self.squeeze_node(node.child_nw)
            self.squeeze_node(node.child_ne)
            self.squeeze_node(node.child_sw)
            self.squeeze_node(node.child_se)
            
    
    def run_quadtree(self):
        """Run the quadtree forward.
        
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
        
        
    def _forward(self, node: QuadNode):
        """Advance quadtree by comparing child nodes and expanding resolution where necessary.
        
        """
        if node._is_split():
            self._compare_nodes(node.child_nw, node.child_ne, False)
            self._compare_nodes(node.child_sw, node.child_se, False)
            self._compare_nodes(node.child_nw, node.child_sw, True)
            self._compare_nodes(node.child_ne, node.child_se, True)
        elif node.depth < self.min_depth:
            node.split_node()
            if self.verbose: self._save_checkpoint()
            
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
                    
                    
    def _get_min_max_nodes(self, node: QuadNode):
        
        if node._is_split():
            self._get_min_max_nodes(node.child_nw)
            self._get_min_max_nodes(node.child_ne)
            self._get_min_max_nodes(node.child_sw)
            self._get_min_max_nodes(node.child_se)
        
        if node.get_node_value() > self.max_node_value:
            self.max_node_value = node.get_node_value()
            
        if node.get_node_value() < self.min_node_value and node.get_node_value() != -np.inf:
            self.min_node_value = node.get_node_value()
                                
    
    def _draw_nodes(self, ax,
                    node: QuadNode,
                    mappable,
                    show_points,
                    show_values
                    ):
        """Draw nodes and children.
        
        """
        
        if node._is_split():
            self._draw_nodes(ax, node.child_nw, mappable, show_points, show_values)
            self._draw_nodes(ax, node.child_ne, mappable, show_points, show_values)
            self._draw_nodes(ax, node.child_sw, mappable, show_points, show_values)
            self._draw_nodes(ax, node.child_se, mappable, show_points, show_values)
            
        node.draw_node(ax, mappable, show_points, show_values)
        
    
    def draw_tree(self, ax,
                  cmap: str = 'RdYlGn_r',
                  vmin: float = None,
                  vmax: float = None,
                  show_points: bool = False,
                  show_values: bool = False,
                  **cb_kwargs
                  ):
        """Draw the entire quadtree.
        
        Args:
            ax (:obj:`matplotlib.pyplot.Axes`): Axis for plotting.
        """
        
        if vmin is None:
            self._get_min_max_nodes(self.root)
            vmin = 0.8 * self.min_node_value
        if vmax is None:
            self._get_min_max_nodes(self.root)
            vmax = 1.2 * self.max_node_value
        
        mappable = mpl.cm.ScalarMappable(
            mpl.colors.Normalize(vmin, vmax),
            cmap=cmap
            )
        
        self._draw_nodes(ax, self.root, mappable, show_points, show_values)
        mpl.pyplot.colorbar(mappable, ax=ax, **cb_kwargs)
