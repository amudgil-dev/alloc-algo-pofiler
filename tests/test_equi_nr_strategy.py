import pytest
import random
from app.algo.equi_nr_strategy import get_equi_no_repacking_servers


def test_integer_input():
    """Test that integer inputs return the same integer."""
    assert get_equi_no_repacking_servers(5) == 5
    assert get_equi_no_repacking_servers(0) == 0
    assert get_equi_no_repacking_servers(100) == 100

def test_fractional_input_deterministic():
    """Test fractional inputs with a fixed random seed for deterministic results."""
    random.seed(42)  # Set a fixed seed for reproducibility
    
    # Test a few fractional inputs
    assert get_equi_no_repacking_servers(3.7) in [3, 4]
    assert get_equi_no_repacking_servers(2.1) in [2, 3]
    assert get_equi_no_repacking_servers(4.9) in [4, 5]

def test_fractional_input_statistical():
    """
    Test fractional inputs statistically to ensure the expected value is correct.
    """
    def run_statistical_test(x, n_trials=10000):
        results = [get_equi_no_repacking_servers(x) for _ in range(n_trials)]
        mean = sum(results) / n_trials
        expected = x
        # Allow for a small margin of error due to randomness
        assert abs(mean - expected) < 0.1, f"Expected ~{expected}, got {mean}"

    run_statistical_test(3.7)
    run_statistical_test(2.1)
    run_statistical_test(4.9)

def test_edge_cases():
    """Test edge cases."""
    assert get_equi_no_repacking_servers(0.1) in [0, 1]
    assert get_equi_no_repacking_servers(0.9) in [0, 1]
    assert get_equi_no_repacking_servers(10.1) in [10, 11]

def test_negative_input():
    """Test that negative inputs raise a ValueError."""
    with pytest.raises(ValueError):
        get_equi_no_repacking_servers(-1)

def test_non_numeric_input():
    """Test that non-numeric inputs raise a TypeError."""
    with pytest.raises(TypeError):
        get_equi_no_repacking_servers("not a number")

@pytest.mark.parametrize("input_value, expected_range", [
    (1.2, (1, 2)),
    (3.8, (3, 4)),
    (7.5, (7, 8)),
    (9.9, (9, 10)),
])
def test_various_inputs(input_value, expected_range):
    """Test various inputs to ensure they fall within the expected range."""
    result = get_equi_no_repacking_servers(input_value)
    assert result in expected_range, f"Expected {result} to be in {expected_range}"

def test_random_seed_independence():
    """Test that the function works correctly with different random seeds."""
    x = 3.5
    results = set()
    for _ in range(100):
        random.seed()  # Reset the random seed
        results.add(get_equi_no_repacking_servers(x))
    assert results == {3, 4}, f"Expected results to be {{3, 4}}, got {results}"
