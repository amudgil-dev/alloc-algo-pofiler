import numpy as np
from scipy import optimize
from scipy.optimize import linprog


def solve_optimal_allocation(d_n, arrival_rate, speedup_factors):
    # Objective function coefficients (minimize sum of y_i)
    c = np.ones(d_n)  # We want to minimize sum(y_i)

    # Coefficients matrix for constraints
    A = np.zeros((2, d_n))

    # Constraint 1: sum(s_i * y_i) = arrival_rate
    A[0, :] = speedup_factors

    # Constraint 2: sum(i * y_i) <= 1
    A[1, :] = np.arange(1, d_n + 1)

    # Bounds for each variable y_i
    bounds = [(0, None) for _ in range(d_n)]

    # Right-hand side values for constraints
    b = [arrival_rate, 1]  # Equals to arrival rate, and utilization <= 1

    # Solve the linear program
    res = linprog(
        c,
        A_eq=[A[0]],
        b_eq=[b[0]],
        A_ub=[A[1]],
        b_ub=[b[1]],
        bounds=bounds,
        method="highs",
    )

    # Check if the optimization was successful
    if res.success:
        print(f"Optimal y values: {res.x}")
        return res.x  # Optimal allocation probabilities
    else:
        print("Optimization failed.")
        return None


# testing:im
d_n = 10  # Maximum degree of parallelism
arrival_rate = 0.8  # Example arrival rate
speedup_factors = [
    i**0.5 for i in range(1, d_n + 1)
]  # Example concave speed-up function

optimal_allocation = solve_optimal_allocation(d_n, arrival_rate, speedup_factors)
