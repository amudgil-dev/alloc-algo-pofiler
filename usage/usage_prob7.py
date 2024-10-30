import numpy as np
import cvxpy as cp
from app.algo.prob7 import solve_problem_7

def example_prob7():

    d_n = 10  # maximum parallelism
    lambda_val = 0.8  # arrival rate
    s = np.array([i**0.8 for i in range(1, d_n + 1)])  # example speed-up function

    optimal_y = solve_problem_7(d_n, lambda_val, s)

    print("Optimal allocation:")
    for i, yi in enumerate(optimal_y):
        # if yi > 1e-6:  # Only print non-zero values
        print(f"y[{i+1}] = {yi:.6f}")

example_prob7()