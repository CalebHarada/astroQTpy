from astroqtpy.quadpoint import QuadPoint

def test_quad_point() -> None:
    """Test the QuadPoint dataclass.
    
    """

    # set ground truth values
    x = 2.3
    y = 3.1
    value = 8.3
    
    # new instanace of QuadPoint with ground truth values
    point = QuadPoint(x, y, value)
    assert point.x == x
    assert point.y == y
    assert point.value == value
    
    # new ground truth values
    x_new = 100.3
    y_new = -4.6
    value_new = 0.0
    
    # set new ground truth values
    point.x = x_new
    point.y = y_new
    point.val = value_new
    assert point.x == x_new
    assert point.y == y_new
    assert point.val == value_new
    
    
    
if __name__ == "__main__":
    test_quad_point()