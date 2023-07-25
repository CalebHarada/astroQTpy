import numpy as np

from astroqtpy.quadnode import QuadNode

from .quadnode import QuadNode
from .quadpoint import QuadPoint
from .basetree import BaseTree


class RandomQuadTree(BaseTree):
    """_summary_

    _extended_summary_

    Args:
        x_min (float): _description_
        x_max (float): _description_
        y_min (float): _description_
        y_max (float): _description_
        split_threshold (float, optional): _description_. Defaults to 0.2.
        node_statistic (str, optional): _description_. Defaults to 'mean'.
        N_points (int, optional): _description_. Defaults to 20.
        min_depth (int, optional): _description_. Defaults to 3.
        max_depth (int, optional): _description_. Defaults to 6.
        N_proc (int, optional): _description_. Defaults to 1.
        verbose (bool, optional): _description_. Defaults to False.
        filename_points (str, optional): _description_. Defaults to 'points.txt'.
        filename_nodes (str, optional): _description_. Defaults to 'nodes.txt'.
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
        """_summary_

        _extended_summary_
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
        """_summary_

        _extended_summary_

        Args:
            node (QuadNode): _description_
            rng_seed (int, optional): _description_. Defaults to 123456.

        Returns:
            QuadPoint: _description_
        """
        
        rng = np.random.default_rng(rng_seed)
        
        point = QuadPoint(
            rng.uniform(node.x_min, node.x_max),
            rng.uniform(node.y_min, node.y_max),
            rng.choice([1, 0])
            )
    
        return point



class NbodyQuadTree(BaseTree):
    """_summary_

    _extended_summary_

    Args:
        x_min (float): _description_
        x_max (float): _description_
        y_min (float): _description_
        y_max (float): _description_
        simulation_fnc (callable): _description_
        split_threshold (float, optional): _description_. Defaults to 0.2.
        node_statistic (str, optional): _description_. Defaults to 'mean'.
        N_points (int, optional): _description_. Defaults to 20.
        min_depth (int, optional): _description_. Defaults to 3.
        max_depth (int, optional): _description_. Defaults to 6.
        N_proc (int, optional): _description_. Defaults to 1.
        verbose (bool, optional): _description_. Defaults to False.
        filename_points (str, optional): _description_. Defaults to 'points.txt'.
        filename_nodes (str, optional): _description_. Defaults to 'nodes.txt'.
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
        """_summary_

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
        
        self.simulation_fnc = simulation_fnc
        
            
    def evaluate_point(self, node: QuadNode, rng_seed: int = 123456) -> QuadPoint:
        """_summary_

        _extended_summary_

        Args:
            node (QuadNode): _description_
            rng_seed (int, optional): _description_. Defaults to 123456.

        Returns:
            QuadPoint: _description_
        """
        
        rng = np.random.default_rng(rng_seed)
        _x = rng.uniform(node.x_min, node.x_max)
        _y = rng.uniform(node.y_min, node.y_max)
        
        sim = self.simulation_fnc((_x, _y))
        
        point = QuadPoint(_x, _y, sim)
    
        return point

        
        
        
        
        