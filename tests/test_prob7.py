import pytest
import numpy as np
import cvxpy as cp
from app.algo.prob7 import solve_problem_7


def test_solve_problem_7_valid():
    d_n = 10
    lambda_val = 0.8
    s = np.array([i**0.8 for i in range(1, d_n + 1)])
    optimal_y = solve_problem_7(d_n, lambda_val, s)
    
    assert len(optimal_y) == d_n
    assert np.all(optimal_y >= 0)
    assert np.isclose(np.sum(s * optimal_y), lambda_val, atol=1e-6)
    assert np.sum(np.arange(1, d_n + 1) * optimal_y) <= 1 + 1e-6

def test_solve_problem_7_edge_case_low_lambda():
    d_n = 10
    lambda_val = 0.1
    s = np.array([i**0.8 for i in range(1, d_n + 1)])
    optimal_y = solve_problem_7(d_n, lambda_val, s)
    
    assert len(optimal_y) == d_n
    assert np.all(optimal_y >= 0)
    assert np.isclose(np.sum(s * optimal_y), lambda_val, atol=1e-6)

def test_solve_problem_7_edge_case_high_lambda():
    d_n = 10
    lambda_val = 5.0
    s = np.array([i**0.8 for i in range(1, d_n + 1)])
    optimal_y = solve_problem_7(d_n, lambda_val, s)
    
    assert len(optimal_y) == d_n
    assert np.all(optimal_y >= 0)
    assert np.isclose(np.sum(s * optimal_y), lambda_val, atol=1e-6)

def test_solve_problem_7_different_speedup():
    d_n = 10
    lambda_val = 0.8
    s = np.array([i**0.5 for i in range(1, d_n + 1)])  # Different speedup function
    optimal_y = solve_problem_7(d_n, lambda_val, s)
    
    assert len(optimal_y) == d_n
    assert np.all(optimal_y >= 0)
    assert np.isclose(np.sum(s * optimal_y), lambda_val, atol=1e-6)

def test_solve_problem_7_small_d_n():
    d_n = 2
    lambda_val = 0.5
    s = np.array([1.0, 2.0])
    optimal_y = solve_problem_7(d_n, lambda_val, s)
    
    assert len(optimal_y) == d_n
    assert np.all(optimal_y >= 0)
    assert np.isclose(np.sum(s * optimal_y), lambda_val, atol=1e-6)

def test_solve_problem_7_large_d_n():
    d_n = 100
    lambda_val = 1.0
    s = np.array([i**0.8 for i in range(1, d_n + 1)])
    optimal_y = solve_problem_7(d_n, lambda_val, s)
    
    assert len(optimal_y) == d_n
    assert np.all(optimal_y >= 0)
    assert np.isclose(np.sum(s * optimal_y), lambda_val, atol=1e-6)

def test_solve_problem_7_infeasible():
    d_n = 10
    lambda_val = -0.8  # Negative lambda should make the problem infeasible
    s = np.array([i**0.8 for i in range(1, d_n + 1)])
    
    with pytest.raises(ValueError):
        solve_problem_7(d_n, lambda_val, s)

def test_solve_problem_7_zero_lambda():
    d_n = 10
    lambda_val = 0
    s = np.array([i**0.8 for i in range(1, d_n + 1)])
    optimal_y = solve_problem_7(d_n, lambda_val, s)
    
    assert len(optimal_y) == d_n
    assert np.all(optimal_y == 0)

def test_solve_problem_7_constant_speedup():
    d_n = 10
    lambda_val = 0.8
    s = np.ones(d_n)  # Constant speedup
    optimal_y = solve_problem_7(d_n, lambda_val, s)
    
    assert len(optimal_y) == d_n
    assert np.all(optimal_y >= 0)
    assert np.isclose(np.sum(s * optimal_y), lambda_val, atol=1e-6)
    assert np.isclose(optimal_y[0], lambda_val, atol=1e-6)  # Only first server should be used
