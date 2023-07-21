import numpy as np
import rebound  # import throws `pkg_resources.declare_namespace` warning

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
        split_threshold (float): _description_. Defaults to 0.2.
        N_points (int, optional): _description_. Defaults to 20.
        min_depth (int, optional): _description_. Defaults to 3.
        max_depth (int, optional): _description_. Defaults to 6.
        N_proc (int, optional): _description_. Defaults to 4.
        verbose (bool, optional): _description_. Defaults to True.
        filename_points (str, optional): _description_. Defaults to 'points.txt'.
        filename_nodes (str, optional): _description_. Defaults to 'nodes.txt'.
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
        
        Create a random quadtree.
        """
        super().__init__(
            x_min, x_max, y_min, y_max, split_threshold,
            N_points, min_depth, max_depth, N_proc, verbose,
            filename_points, filename_nodes
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
        split_threshold (float): _description_. Defaults to 0.2.
        N_points (int, optional): _description_. Defaults to 20.
        min_depth (int, optional): _description_. Defaults to 3.
        max_depth (int, optional): _description_. Defaults to 6.
        N_proc (int, optional): _description_. Defaults to 4.
        verbose (bool, optional): _description_. Defaults to True.
        filename_points (str, optional): _description_. Defaults to 'points.txt'.
        filename_nodes (str, optional): _description_. Defaults to 'nodes.txt'.
    """
    
    def __init__(self,
            x_min: float,
            x_max: float,
            y_min: float,
            y_max: float,
            particles: list[dict],
            x_var: dict,
            y_var: dict,
            duration: float = 5e2,
            integrator: str = 'ias15',
            timestep: float = 5.,
            exit_max_distance: float = 20.,
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
        
        Create an N-body simulation quadtree.
        """
        super().__init__(
            x_min, x_max, y_min, y_max, split_threshold,
            N_points, min_depth, max_depth, N_proc, verbose,
            filename_points, filename_nodes
            )
        
        self.particles = particles
        self.x_var = x_var
        self.y_var = y_var
        self.sim_duration = duration
        self.integrator = integrator
        self.timestep = timestep
        self.exit_max_distance = exit_max_distance
        
        
    def setup_simulation(self):
        
        sim = rebound.Simulation()
        
        sim.integrator = self.integrator
        if self.integrator == 'whfast':
            sim.ri_whfast.safe_mode = 0
            
        sim.dt = self.timestep
        
        for particle in self.particles:
            sim.add(**particle)
            
        sim.move_to_com()
        sim.init_megno()
        sim.exit_max_distance = self.exit_max_distance
        
        return sim
        
        
    def run_simulation(self, simulation):
        
        try:
            simulation.integrate(self.sim_duration * 2*np.pi)
            megno = simulation.calculate_megno()
            return megno
        except rebound.Escape:
            return 10. # At least one particle got ejected, returning large MEGNO.
            
    
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
        
        sim = self.setup_simulation()
        setattr(sim.particles[self.x_var['particle']], self.x_var['variable'], _x)
        setattr(sim.particles[self.y_var['particle']], self.y_var['variable'], _y)
        result = self.run_simulation(sim)
        
        point = QuadPoint(_x, _y, result)
    
        return point

        
        
        
        
        