import cvxpy as cp
import numpy as np


def solve_problem_7(d_n, lambda_val, s):
    # Define variables
    # create yi vector of length d_n
    y = cp.Variable(d_n)

    # Define objective
    objective = cp.Minimize((1 / lambda_val) * cp.sum(y))

    # Define constraints
    constraints = [
        # c1: rtc constraint
        cp.sum(cp.multiply(s, y)) == lambda_val,
        # c2: busy servers/total servers
        cp.sum(cp.multiply(np.arange(1, d_n + 1), y)) <= 1,
        # c3: non neg yis
        y >= 0,
    ]

    # Define and solve the problem
    problem = cp.Problem(objective, constraints)
    problem.solve()

    # Check if the problem was solved successfully
    if problem.status != cp.OPTIMAL:
        raise ValueError("Problem did not solve successfully")

    return y.value


# Example usage:
d_n = 10  # maximum parallelism
lambda_val = 0.8  # arrival rate
s = np.array([i**0.8 for i in range(1, d_n + 1)])  # example speed-up function

optimal_y = solve_problem_7(d_n, lambda_val, s)

print("Optimal allocation:")
for i, yi in enumerate(optimal_y):
    # if yi > 1e-6:  # Only print non-zero values
    print(f"y[{i+1}] = {yi:.6f}")
