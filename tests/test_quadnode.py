import pytest
from astroqtpy.quadnodes import NbodyNode
from astroqtpy.base import QuadPoint
import matplotlib.pyplot as plt

def test_nbody_node() -> None:
    """Test the Nbody QuadNode class
    
    """
    # test instantiation of Nbody Node
    my_node = NbodyNode(0, 1, 0, 1)
    
    # test node splitting
    assert my_node._is_split() == False
    my_node.split_node()
    assert my_node._is_split() == True
    
    # test node value generation
    my_node.node_points.append(QuadPoint(0.5, 0.5, 12))
    my_node.node_points.append(QuadPoint(0.25, 0.75, 15))
    my_node.node_points.append(QuadPoint(0.1, 0.6, 16))
    
    my_node.generate_node_value()  # should be 14.333334
    assert my_node._get_node_value() == pytest.approx(14.333334)
    
    
if __name__ == "__main__":
    test_nbody_node()