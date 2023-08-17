import pytest
import matplotlib.pyplot as plt
import numpy as np

from astroqtpy.quadtree import Hist2dQuadTree


def test_hist2dquadtree() -> None:
    """Test histogram quad tree class.
    
    """
    
    # creat instance
    test_tree = Hist2dQuadTree(0, 1, 0, 1,
                               min_depth=1,
                               max_depth=8,
                               N_points=5
                               )
    
    # make up data
    N_points = 5000
    x = np.random.normal(0.5, 0.1, N_points)
    y = np.random.normal(0.5, 0.1, N_points)
    
    # add it to the quadtree
    test_tree.add_data(x, y)
    
    # make figure
    fig, ax = plt.subplots()
    test_tree.draw_tree(ax, show_colors=False)
    fig.savefig('./tests/end-to-end-tests/test_outputs/hist2dtree_plot.png', dpi=200)
    
    
    
if __name__ == "__main__":
    test_hist2dquadtree()

