import numpy as np

from astroqtpy.quadnode import QuadNode

from .quadnode import QuadNode
from .quadpoint import QuadPoint
from .basetree import BaseTree


class RandomQuadTree(BaseTree):
    """Random quadtree.

    A class for creating a quadtree with randomly sampled points.

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

        Create this random quadtree.
        """
        
        super().__init__(x_min,
                         x_max,
                         y_min,
                         y_max,
                         split_threshold,
                         node_statistic,
                         N_points,
                         min_depth,
                         max_depth,
                         N_proc,
                         verbose,
                         filename_points,
                         filename_nodes
                         )
        
        
    def evaluate_point(self, node: QuadNode, rng_seed: int = 123456) -> QuadPoint:
        """Evaluate point.

        Calculate the value of one point within a given node as either 1 or 0.

        Args:
            node (QuadNode): Quadtree node in which to evaulate point.
            rng_seed (int, optional): Random number generator seed. Defaults to 123456.

        Returns:
            QuadPoint: A QuadPoint object.
        """
        
        rng = np.random.default_rng(rng_seed)
        
        point = QuadPoint(
            rng.uniform(node.x_min, node.x_max),
            rng.uniform(node.y_min, node.y_max),
            rng.choice([1, 0])
            )
    
        return point



class NbodyQuadTree(BaseTree):
    """Nbody quadtree.

    A class for creating a quadtree for running N-body simulations.

    Args:
        x_min (float): Minimum x value for this quadtree.
        x_max (float): Maximum x value for this quadtree.
        y_min (float): Minimum y value for this quadtree.
        y_max (float): Maximum y value for this quadtree.
        simulation_fnc (callable): Function to calculate the outcome of an Nbody simulation.
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
                 simulation_fnc: callable,
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

        Create an N-body simulation quadtree.
        """
        
        super().__init__(x_min,
                         x_max,
                         y_min,
                         y_max,
                         split_threshold,
                         node_statistic,
                         N_points,
                         min_depth,
                         max_depth,
                         N_proc,
                         verbose,
                         filename_points,
                         filename_nodes)
        
        # check that input function is callable
        if not callable(simulation_fnc):
            raise TypeError('simulation_fnc must be callable.')
        else:
            self.simulation_fnc = simulation_fnc
        
            
    def evaluate_point(self, node: QuadNode, rng_seed: int = 123456) -> QuadPoint:
        """Evaluate point.

        Calculate the value of one point within a given node from an N-body simulation.

        Args:
            node (QuadNode): Quadtree node in which to evaulate point.
            rng_seed (int, optional): Random number generator seed. Defaults to 123456.

        Returns:
            QuadPoint: A QuadPoint object.
        """
        
        rng = np.random.default_rng(rng_seed)
        _x = rng.uniform(node.x_min, node.x_max)
        _y = rng.uniform(node.y_min, node.y_max)
        
        # run N-body sim
        sim = self.simulation_fnc((_x, _y))
        
        point = QuadPoint(_x, _y, sim)
    
        return point

        
        
        
        
        