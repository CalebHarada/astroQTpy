import pytest
import matplotlib.pyplot as plt

from astroqtpy.quadtree import RandomQuadTree


def test_randomquadtree() -> None:
    """Test random quad tree class.
    
    """
    
    # creat instance
    test_tree = RandomQuadTree(0, 1, 0, 1,
                               N_proc=1,
                               filename_points='./tests/end-to-end-tests/test_outputs/randomtree_points.txt',
                               filename_nodes='./tests/end-to-end-tests/test_outputs/randomtree_nodes.txt'
                               )
    with pytest.raises(ValueError):
        test_tree = RandomQuadTree(1, 1, 0, 1)
    with pytest.raises(ValueError):
        test_tree = RandomQuadTree(0, 1, 0, 1, split_threshold=-10)
    with pytest.raises(ValueError):
        test_tree = RandomQuadTree(0, 1, 0, 1, node_statistic='fake_statistic')
    with pytest.raises(ValueError):
        test_tree = RandomQuadTree(0, 1, 0, 1, N_points=-1)
    with pytest.raises(ValueError):
        test_tree = RandomQuadTree(0, 1, 0, 1, min_depth=6, max_depth=3)
    with pytest.raises(ValueError):
        test_tree = RandomQuadTree(0, 1, 0, 1, N_proc=-4)
    
    # run tree
    test_tree.run_quadtree()
    
    # make figure
    fig, ax = plt.subplots()
    test_tree.draw_tree(ax, show_points=True)
    fig.savefig('./tests/end-to-end-tests/test_outputs/randomtree_plot.png', dpi=200)
    
    
    
if __name__ == "__main__":
    test_randomquadtree()

