import pytest
import matplotlib.pyplot as plt
import numpy as np

from astroqtpy.quadtree import Chi2QuadTree


def calc_model(x, params):
    """model function for Chi2QuadTree test. See tutorial notebook for further details.
    
    """
    a, b = params # unpack parameters
    
    # simplest 2-parameter fit: line
    y = a * x + b
    
    return y


def test_chi2quadtree() -> None:
    """Test chi2 quad tree class.
    
    """
    # mock data
    a_truth = 1.4
    b_truth = 2.3
    sigma = 0.4
    N_data = 100

    x_data = np.linspace(0, 10, N_data)
    y_data = calc_model(x_data, (a_truth, b_truth)) + np.random.normal(0, sigma, N_data)
    data = np.stack((x_data, y_data))
    weights = np.full(N_data, 1/sigma**2)
    
    # plt.errorbar(*data, yerr=sigma, fmt='.')
    # plt.show()
    
    # creat instance
    test_tree = Chi2QuadTree(0.5, 2.5, 0, 5,
                             data,
                             calc_model,
                             weights=weights,
                             split_threshold=0.5,
                             N_proc=1,
                             filename_points='./tests/end-to-end-tests/test_outputs/chi2tree_points.txt',
                             filename_nodes='./tests/end-to-end-tests/test_outputs/chi2tree_nodes.txt'
                             )    
    with pytest.raises(ValueError):
        test_tree = Chi2QuadTree(0.5, 2.5, 7, 5, data, calc_model)
    with pytest.raises(ValueError):
        test_tree = Chi2QuadTree(0.5, 2.5, 0, 5, data.T, calc_model, weights=weights)
    with pytest.raises(ValueError):
        test_tree = Chi2QuadTree(0.5, 2.5, 0, 5, data, calc_model, weights=weights[1:])
    with pytest.raises(ValueError):
        test_tree = Chi2QuadTree(0.5, 2.5, 0, 5, data, calc_model, weights=weights, max_chi2=0)
    with pytest.raises(TypeError):
        test_tree = Chi2QuadTree(0.5, 2.5, 0, 5, data, "calc_model", weights=weights)
    
    # run tree
    test_tree.run_quadtree()
    
    # make figure
    fig, ax = plt.subplots()
    map = test_tree.draw_tree(ax)
    plt.colorbar(map, ax=ax, label='chi^2')
    fig.savefig('./tests/end-to-end-tests/test_outputs/chi2tree_plot.png', dpi=200)
    
    
    
if __name__ == "__main__":
    test_chi2quadtree()

