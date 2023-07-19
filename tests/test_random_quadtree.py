from astroqtpy.quadtree import RandomQuadTree
import matplotlib.pyplot as plt

def test_randomquadtree() -> None:
    """Test random quad tree class
    
    """
    
    test_tree = RandomQuadTree(0, 1, 0, 1, 0.2, N_proc=1)
    
    #test_tree.run_quadtree()
    
    #_, ax = plt.subplots()
    #test_tree.draw_tree(ax)
    #plt.show()
    


if __name__ == "__main__":
    test_randomquadtree()
