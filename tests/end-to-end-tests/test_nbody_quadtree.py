import matplotlib.pyplot as plt
import numpy as np
import rebound

from astroqtpy.quadtree import NbodyQuadTree

def simulation(par):
    """Simulation function for NbodyQuadTree test. See tutorial notebook for further details.
    
    """

    a, e = par # unpack parameters
    sim = rebound.Simulation()
    sim.integrator = "whfast"
    sim.ri_whfast.safe_mode = 0
    sim.dt = 5.
    sim.add(m=1.) # Star
    sim.add(m=0.001045, a=4.489, M=0.2, omega=0.277, e=0.058) # Planet inner
    sim.add(m=0.000584, a=a, M=0.781, omega=3.25, e=e) # Planet outer
    sim.move_to_com()

    sim.init_megno()
    sim.exit_max_distance = 20.

    try:
        sim.integrate(5e3 * 2.*np.pi, exact_finish_time=0) # integrate
        megno = sim.calculate_megno()
        return megno

    except rebound.Escape:
        return 50. # At least one particle got ejected, returning large MEGNO.
    
    
def test_nbodyquadtree() -> None:
    """Test N-body quad tree class.
    
    """
        
    # define parameter space
    x_min, x_max = 5, 15
    y_min, y_max = 0, 0.5
    
    # initialize NbodyQuadTree
    test_tree = NbodyQuadTree(x_min, x_max, y_min, y_max, simulation,
                              split_threshold=0.5,
                              N_points=20,
                              N_proc=4,
                              max_depth=6,
                              verbose=True,
                              filename_points='./tests/end-to-end-tests/test_outputs/nbodytree_points.txt',
                              filename_nodes='./tests/end-to-end-tests/test_outputs/nbodytree_nodes.txt'
                              )
    
    test_tree.run_quadtree()  # test multiprocessing option
    
    # make figure
    fig, ax = plt.subplots()
    quadtree_map = test_tree.draw_tree(ax, vmin=1, vmax=20)
    plt.colorbar(quadtree_map, ax=ax, label='Average MEGNO')
    ax.set_xlabel('$a$')
    ax.set_ylabel('$e$')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    fig.savefig('./tests/end-to-end-tests/test_outputs/nbodytree_plot.png', dpi=200)
    

if __name__ == "__main__":
    test_nbodyquadtree()

