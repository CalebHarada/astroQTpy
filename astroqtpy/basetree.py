import abc

import numpy as np
from rebound.interruptible_pool import InterruptiblePool

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
        split_threshold : float,
        N_points : int = 20,
        min_depth : int = 3,
        max_depth : int = 6,
        N_proc : int = 4,
        verbose: bool = True,
        
        ) -> None:
        """__init__

        Create the base quadtree node for astroQTpy.
        """
        
        super().__init__()
        
        self.split_threshold = split_threshold
        self.N_points = N_points
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.N_proc = N_proc
        self.verbose = verbose
        
        self.node_count = 1
        
        
    
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
                self.evaluate_one_point(node, rng_seed=np.random.randint(1, 1e8))
     
     
    def evaluate_multiple_points(self, node: QuadNode, N_points: int):
        """Evaluate multiple points within a node in parallel.
        
        """
        N_empty = int(N_points - len(node.node_points))
        map_iters = [(node, np.random.randint(1, 1e8)) for _ in range(N_empty)]
        
        with InterruptiblePool(processes=self.N_proc) as pool:
            points = pool.starmap(self.evaluate_one_point, map_iters)
            for point in points:
                node.node_points.append(point)
                
                
    @abc.abstractmethod
    def evaluate_one_point(self, node: QuadNode, rng_seed: int = 123456, iter: int = -1) -> None:
        """Abstract method to calculate the value of one point within a given node.
        
        """
        pass
    
    
    def _save_checkpoint(self):
        """Convenience function to save progress and update node count
        (called any time a node is split).
        
        """
        self.node_count = self.node_count + 3
        self.print_all_nodes()
        self.print_all_points()
        print(f"Progress saved. (nodes = {self.node_count})")
    