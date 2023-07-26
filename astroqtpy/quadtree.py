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





class Chi2QuadTree(BaseTree):
    """Chi2 quadtree.
    
    A quadtree class for mapping 2-parameter reduced :math:`\\chi^2` values.
    
    .. math::
        \\chi^2_r = \\frac{\\chi^2}{\\nu}
        
    where :math:`\\nu` is the number of degrees of freedom and
    
    .. math::
        \\chi^2 = \\sum_{i=0}^{N-1} \\frac{\\Big(y_i - f(x_i | a, b)\\Big)^2}{\\sigma_i^2}
        
    .. note::
    
        The `model_func` argument must be callable and take two arguments: `x_data` and parameters `(a, b)`.
        It must return a single float value `y`. For example:
        
        .. code-block:: python
        
            def my_model(x, parameters):
                a, b = parameters  # unpack parameters
                
                # ... do something ...
                y = a * x + b
                
                return y
                
        See tutorials for more examples.
        
    Args:
        x_min (float): Minimum x value (param `a`) for this quadtree.
        x_max (float): Maximum x value (param `a`)for this quadtree.
        y_min (float): Minimum y value (param `b`)for this quadtree.
        y_max (float): Maximum y value (param `b`)for this quadtree.
        data (:obj:`np.ndarray`): Data array. Must have shape (2, N).
        model_func (callable): Function :math:`f(x | a, b)` to calculate a model to compare to data.
        weights (:obj:`np.ndarray`, optional): Data weights, typically expressed as :math:`1/\\sigma^2`. Defaults to None.
        max_chi2 (float, optional): Largest permitted reduced :math:`\\chi^2`. Defaults to 10.
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
                 data: np.ndarray,
                 model_func: callable,
                 weights: np.ndarray = None,
                 max_chi2: float = 10,
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

        Create a chi-squared quadtree.
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
        
        # check inputs
        if not type(data) == np.ndarray:
            raise TypeError('data must be ndarray.')
        elif np.shape(data)[0] != 2:
            raise ValueError('data array must have shape (2, N).')
        else:
            self.data = data
        
        if not callable(model_func):
            raise TypeError('model_func must be callable.')
        else:
            self.model_func = model_func
            
        if weights is not None:
            if len(weights) != np.shape(data)[1]:
                raise ValueError('length of weights array must be equal to data.')
            else:
                self.weights = weights
        else:
            self.weights = np.ones(np.shape(data)[1])
            
        if max_chi2 <= 0:
            raise ValueError('max_chi2 must be greater than zero.')
        else:
            self.max_chi2 = max_chi2
            
        # define other attributes
        self.chi2_min_point = QuadPoint(0, 0, np.inf)  # just a dummy point for now
        
    
    def evaluate_point(self, node: QuadNode, rng_seed: int = 123456) -> QuadPoint:
        """Evaluate point.

        Calculate the value of one point within a given node.

        Args:
            node (QuadNode): Quadtree node in which to evaulate point.
            rng_seed (int, optional): Random number generator seed. Defaults to 123456.

        Returns:
            QuadPoint: A QuadPoint object.
        """
        rng = np.random.default_rng(rng_seed)
        _x = rng.uniform(node.x_min, node.x_max)
        _y = rng.uniform(node.y_min, node.y_max)
        
        # grab data
        x_data = self.data[0]
        y_data = self.data[1]
        
        # calculate model
        model_params = (_x, _y)
        y_model = self.model_func(x_data, model_params)
        
        # calculate chi-squared
        dof = len(y_data) - 2
        chi2 = np.sum(self.weights * (y_data - y_model)**2)
        
        # reduced chi-square
        chi2_r = np.min((self.max_chi2, chi2 / dof))  # if really large, set to max_chi2
        
        point = QuadPoint(_x, _y, chi2_r)
    
        return point
    
    
    def _find_chi2_min(self, node: QuadNode) -> None:
        """Find chi^2 min.

        Convenience function to locate the point with the smallest chi^2 value.

        Args:
            node (QuadNode): Quadtree node.
        """
        
        if node._is_split():
            self._find_chi2_min(node.child_nw)
            self._find_chi2_min(node.child_ne)
            self._find_chi2_min(node.child_sw)
            self._find_chi2_min(node.child_se)
        
        for point in node.node_points:
            if point.value < self.chi2_min_point.value:
                self.chi2_min_point = point
            
    
    def get_chi2_min(self) -> QuadPoint:
        """Get chi^2 min.

        Get the point with the smallest reduced chi^2 value.
        
        Returns:
            QuadPoint: Quadtree point with least chi^2.
        """
        
        if not np.isfinite(self.chi2_min_point.value):
            self._find_chi2_min(self.root)
            
        return self.chi2_min_point
        
        
        





class NbodyQuadTree(BaseTree):
    """Nbody quadtree.

    A class for creating a quadtree for running N-body simulations.
    
    .. note::
    
        The `simulation_func` argument must be callable and take a single argument `(x, y)`.
        It must return a single float value. For example:
        
        .. code-block:: python
        
            def my_function(parameters):
                x, y = parameters  # unpack parameters
                
                # ... do something ...
                number = float(1)
                
                return number
                
        See tutorials for more examples.


    Args:
        x_min (float): Minimum x value for this quadtree.
        x_max (float): Maximum x value for this quadtree.
        y_min (float): Minimum y value for this quadtree.
        y_max (float): Maximum y value for this quadtree.
        simulation_func (callable): Function to calculate the outcome of an Nbody simulation.
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
                 simulation_func: callable,
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
        if not callable(simulation_func):
            raise TypeError('simulation_func must be callable.')
        else:
            self.simulation_func = simulation_func
        
            
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
        sim = self.simulation_func((_x, _y))
        
        point = QuadPoint(_x, _y, sim)
    
        return point

        
        
        
        
        