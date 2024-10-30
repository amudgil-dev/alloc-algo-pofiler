import pytest
import random
from app.algo.pstar_strategy import speedUp, getPStarVector, getPstar_p1, init_Pstar, getOptimalServerNum

# Test cases for speedUp function
def test_speedUp():
    assert speedUp(1) == 1.0
    assert speedUp(2) == 2**0.8
    assert speedUp(10) == 10**0.8

# Test cases for getPStarVector function
def test_getPStarVector():
    d_n = 10
    arrival_rate = 0.8
    
    # Test case 1: arrival rate below last slope
    p_star = getPStarVector(d_n, 0.1, speedUp)
    assert len(p_star) == d_n
    assert sum(p_star) == pytest.approx(1.0)
    assert all(p == 0 for p in p_star[:-1])
    assert p_star[-1] > 0

    # Test case 2: arrival rate matches a slope
    p_star = getPStarVector(d_n, speedUp(5)/5, speedUp)
    assert len(p_star) == d_n
    assert sum(p_star) == pytest.approx(1.0)
    assert p_star[4] > 0
    assert all(p == 0 for i, p in enumerate(p_star) if i != 4)

    # Test case 3: arrival rate between two slopes
    p_star = getPStarVector(d_n, 0.8, speedUp)
    assert len(p_star) == d_n
    assert sum(p_star) == pytest.approx(1.0)
    assert sum(p > 0 for p in p_star) == 2

# Test cases for getPstar_p1 function
def test_getPstar_p1():
    p_star = [0, 0.6, 0.4, 0, 0]
    p1 = getPstar_p1(p_star)
    assert p1 == [0.6, 2]

    p_star = [0, 0, 0, 1.0, 0]
    p1 = getPstar_p1(p_star)
    assert p1 == [1.0, 4]

# Test cases for init_Pstar function
def test_init_Pstar():
    d_n = 10
    arrival_rate = 0.8
    p1 = init_Pstar(d_n, arrival_rate, speedUp)
    assert len(p1) == 2
    assert 0 < p1[0] <= 1
    assert 1 <= p1[1] <= d_n

# Test cases for getOptimalServerNum function
def test_getOptimalServerNum(monkeypatch):
    def mock_random(a, b):
        return 0.4
    monkeypatch.setattr(random, "uniform", mock_random)

    p1 = [0.5, 3]
    assert getOptimalServerNum(p1) == 3

    p1 = [0.3, 2]
    assert getOptimalServerNum(p1) == 3

# Test the entire workflow
def test_workflow():
    d_n = 10
    arrival_rate = 0.8
    p1 = init_Pstar(d_n, arrival_rate, speedUp)
    assert len(p1) == 2
    assert 0 < p1[0] <= 1
    assert 1 <= p1[1] <= d_n

    optimal_servers = getOptimalServerNum(p1)
    assert 1 <= optimal_servers <= d_n