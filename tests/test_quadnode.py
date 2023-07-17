import pytest
from astroqtpy.nodes import NbodyNode

def test_nbody_node():
    """Test the Nbody QuadNode class
    
    """
    my_node = NbodyNode(0, 1, 0, 1)
    
    assert my_node.is_split() == False
    
    
    
if __name__ == "__main__":
    test_nbody_node()