import pytest
import numpy as np

from astroqtpy.quadnode import QuadNode
from astroqtpy.quadpoint import QuadPoint

def test_nbody_node() -> None:
    """Test the QuadNode class
    
    """
    # test instantiation of Nbody Node
    my_node = QuadNode(0, 1, 0, 1)
    with pytest.raises(ValueError):
        my_node = QuadNode(0, -1, 0, 1)
    with pytest.raises(ValueError):
        my_node = QuadNode(0, 1, 0, -1)
    with pytest.raises(ValueError):
        my_node = QuadNode(0, 0, 0, 1)
    with pytest.raises(ValueError):
        my_node = QuadNode(0, 1, 0, 0)
    with pytest.raises(ValueError):
        my_node = QuadNode(-np.inf, 1, 0, 1)
    with pytest.raises(ValueError):
        my_node = QuadNode(0, 1, 0, np.inf)
    
    # test node splitting
    assert my_node._is_split() == False
    my_node.split_node()
    assert my_node._is_split() == True
    
    # test node value generation
    my_node.node_points.append(QuadPoint(0.5, 0.5, 12))
    my_node.node_points.append(QuadPoint(0.25, 0.75, 15))
    my_node.node_points.append(QuadPoint(0.1, 0.6, 16))
    my_node._generate_node_value('mean')  # should be 14.333334
    assert my_node.get_node_value('mean') == pytest.approx(14.333334)
    with pytest.raises(ValueError):
        my_node._generate_node_value('fake_statistic')  # should throw value error
    
    
if __name__ == "__main__":
    test_nbody_node()