import matplotlib.pyplot as plt

from astroqtpy.quadtree import RandomQuadTree


def test_randomquadtree() -> None:
    """Test random quad tree class.
    
    """
    
    test_tree = RandomQuadTree(0, 1, 0, 1,
                               N_proc=1,
                               filename_points='./tests/end-to-end-tests/test_outputs/randomtree_points.txt',
                               filename_nodes='./tests/end-to-end-tests/test_outputs/randomtree_nodes.txt'
                               )
    test_tree.run_quadtree()
    
    # make figure
    fig, ax = plt.subplots()
    test_tree.draw_tree(ax, show_points=True)
    fig.savefig('./tests/end-to-end-tests/test_outputs/randomtree_plot.png', dpi=200)
    
    
    
if __name__ == "__main__":
    test_randomquadtree()

