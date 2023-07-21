import matplotlib.pyplot as plt
import numpy as np

from astroqtpy.quadtree import NbodyQuadTree


def test_nbodyquadtree() -> None:
    """Test N-body quad tree class.
    
    """
        
    # define particles
    particles = [
        dict(m=1.0, hash='star'),
        dict(m=0.000954, a=5.204, M=0.600, omega=0.257, e=0.048, hash='planet_inner'),
        dict(m=0.000285, a=10., M=0.871, omega=1.616, e=0.1, hash='planet_outer')
    ]
    
    # specify x and y variables
    x_var = dict(particle='planet_outer', variable='a')
    y_var = dict(particle='planet_outer', variable='e')
    
    # define parameter range
    x_min, x_max = 7, 10
    y_min, y_max = 0, 0.5
    
    # initialize NbodyQuadTree
    test_tree = NbodyQuadTree(x_min, x_max, y_min, y_max, particles, x_var, y_var,
                              split_threshold=0.5,
                              integrator='whfast',
                              N_points=12,
                              max_depth=6,
                              duration=50,
                              filename_points='./tests/end-to-end-tests/test_outputs/nbodytree_points.txt',
                              filename_nodes='./tests/end-to-end-tests/test_outputs/nbodytree_nodes.txt'
                              )
    
    test_tree.run_quadtree()
    
    # make figure
    fig, ax = plt.subplots()
    test_tree.draw_tree(ax, vmin=1.9, vmax=4, show_points=False, **dict(label='Average MEGNO'))
    ax.set_xlabel('$a$')
    ax.set_ylabel('$e$')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    fig.savefig('./tests/end-to-end-tests/test_outputs/nbodytree_plot.png', dpi=200)
    

if __name__ == "__main__":
    test_nbodyquadtree()
