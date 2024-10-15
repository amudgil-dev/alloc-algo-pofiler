job_classes = {
    "A": JobClass(
        "A",
        arrival_rate=0.8,
        mean_size=1,
        parallelism=5,
        speedup_function=lambda x: x**0.8,
        generate_job_size_function=lambda: generate_exponential_job_size(1),
    ),
    "B": JobClass(
        "B",
        arrival_rate=0.1,
        mean_size=2,
        parallelism=80,
        speedup_function=lambda x: x**0.7,
        generate_job_size_function=lambda: generate_exponential_job_size(2),
    ),
    "C": JobClass(
        "C",
        arrival_rate=0.7,
        mean_size=1.5,
        parallelism=10,
        speedup_function=lambda x: x**0.9,
        generate_job_size_function=lambda: generate_exponential_job_size(1.5),
    ),
    "D": JobClass(
        "D",
        arrival_rate=0.5,
        mean_size=0.5,
        parallelism=3,
        speedup_function=lambda x: x**0.6,
        generate_job_size_function=lambda: generate_exponential_job_size(0.5),
    ),
    "E": JobClass(
        "E",
        arrival_rate=0.6,
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