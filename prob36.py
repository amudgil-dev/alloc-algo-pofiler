import cvxpy as cp
import numpy as np
from hetroJobs import JobClassManager, JobClass, generate_exponential_job_size


def solve_optimal_allocation(n, job_classes):
    print(f"Starting optimization for {len(job_classes)} job classes with {n} servers")

    # Define variables
    # create a CVXPY Variable for each job class with dimension equal to the parallelism of the job class
    y = {k: cp.Variable(jc.parallelism) for k, jc in job_classes.items()}
    print("Variables defined")

    # Define objective
    objective = cp.Minimize(
        sum(cp.sum(y[k]) / (jc.arrival_rate) for k, jc in job_classes.items())
    )
    print("Objective function defined")

    # Define constraints
    capacity_constraints = []
    rtc_constraints = []
    non_neg_constraints = []
    for k, jc in job_classes.items():
        capacity_constraints.append(
            # c1: busy servers <= total servers
            cp.sum([i * y[k][i - 1] for i in range(1, jc.parallelism + 1)])
            <= n
        )
        rtc_constraints.append(
            # c2: departure rate = arrival rate noramlised by job size
            cp.sum(
                [
                    jc.speedup_values[i - 1] * y[k][i - 1]
                    for i in range(1, jc.parallelism + 1)
                ]
            )
            == (jc.arrival_rate / jc.mean_size)
        )
        # c3: non neg yis
        non_neg_constraints.append(y[k] >= 0)

    # assign constraints
    constraints = capacity_constraints + rtc_constraints + non_neg_constraints

    print(f"Constraints defined: {len(constraints)} constraints in total")

    # Define and solve the problem
    problem = cp.Problem(objective, constraints)
    print("Problem defined, starting solver...")
    problem.solve()
    print(f"Solver status: {problem.status}")

    # Check if the problem was solved successfully
    if problem.status != cp.OPTIMAL:
        raise ValueError("Problem did not solve successfully")

    result = {k: yk.value for k, yk in y.items()}
    print("Optimization complete. Results:")
    for k, v in result.items():
        print(f"Job Class {k}:")
        for i, yi in enumerate(v):
            if yi > 1e-6:  # Only print non-zero values
                print(f"  y[{i+1}] = {yi:.6f}")

    return result


job_classes = {
    "A": JobClass(
        "A",
        arrival_rate=0.1,
        mean_size=1,
        parallelism=5,
        speedup_function=lambda x: x**0.8,
        generate_job_size_function=lambda: generate_exponential_job_size(1),
    ),
    "B": JobClass(
        "B",
        arrival_rate=0.1,
        mean_size=2,
        parallelism=8,
        speedup_function=lambda x: x**0.7,
        generate_job_size_function=lambda: generate_exponential_job_size(2),
    ),
    "C": JobClass(
        "C",
        arrival_rate=0.05,
        mean_size=1.5,
        parallelism=10,
        speedup_function=lambda x: x**0.9,
        generate_job_size_function=lambda: generate_exponential_job_size(1.5),
    ),
    "D": JobClass(
        "D",
        arrival_rate=0.15,
        mean_size=0.5,
        parallelism=3,
        speedup_function=lambda x: x**0.6,
        generate_job_size_function=lambda: generate_exponential_job_size(0.5),
    ),
    "E": JobClass(
        "E",
        arrival_rate=0.1,
        mean_size=1.2,
        parallelism=6,
        speedup_function=lambda x: x**0.75,
        generate_job_size_function=lambda: generate_exponential_job_size(1.5),
    ),
}
n = 100

# Precompute speedup values for each job class
for jc in job_classes.values():
    jc.speedup_values = [jc.speedup_function(i) for i in range(1, jc.parallelism + 1)]

optimal_y = solve_optimal_allocation(n, job_classes)

# for k, v in optimal_y.items():
#     print(k, v)

# Compute pij values
for k, y_values in optimal_y.items():
    jc = job_classes[k]
    rho_j = jc.arrival_rate / jc.mean_size
    p_values = []

    for i in range(jc.parallelism):
        sij = jc.speedup_values[i]
        yij = y_values[i]
        pij = sij * yij / rho_j
        p_values.append(pij)

    print(f"\nJob Class {k}:")
    print("yij values:", y_values)
    print("pij values:", p_values)
    print(f"Sum of pij: {sum(p_values):.6f}")  # This should be close to 1

# Verify that the sum of all pij across all job classes is close to 1
total_p_sum = sum(
    sum(
        sij * yij / (jc.arrival_rate / jc.mean_size)
        for i, (sij, yij) in enumerate(zip(jc.speedup_values, optimal_y[k]))
    )
    for k, jc in job_classes.items()
)
print(f"\nTotal sum of all pij across job classes: {total_p_sum:.6f}")
