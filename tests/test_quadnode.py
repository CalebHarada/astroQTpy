import pytest
from astroqtpy.quadnodes import NbodyNode
import matplotlib.pyplot as plt

def test_nbody_node() -> None:
    """Test the Nbody QuadNode class
    
    """
    
    # test instantiation of Nbody Node
    my_node = NbodyNode(0, 1, 0, 1)
    
    assert my_node.is_split() == False
    
    
if __name__ == "__main__":
    test_nbody_node()