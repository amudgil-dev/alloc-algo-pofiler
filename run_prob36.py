# from app.models.hetro_jobs import JobClassManager, JobClass
from app.algo.prob36 import solve_optimal_allocation
from simdata.sim_parameters import RunParamA


# Precompute speedup values for each job class
job_classes = RunParamA.get_job_classes()

for jc in job_classes.values():
    jc.speedup_values = [jc.speedup_function(i) for i in range(1, jc.parallelism + 1)]
    print("--------------------------------------------------------------")
    print(jc.speedup_values)
    print("*******************************************")

optimal_y = solve_optimal_allocation(job_classes)

# for k, v in optimal_y.items():
#     print(k, v)

my_bjs = []
for k, y_values in optimal_y.items():
    print(f" For class {k} : ")
    jc = job_classes[k]
    rho_j = jc.arrival_rate / jc.mean_size
    bj = 0

    for i in range(jc.parallelism):
        sij = jc.speedup_values[i]
        yij = y_values[i]
        pij = sij * yij / rho_j
        bj += (i + 1) * yij
    my_bjs.append((i + 1) * yij)


sum_of_rhoj = 0
# Compute pij values
for k, y_values in optimal_y.items():
    jc = job_classes[k]
    rho_j = jc.arrival_rate / jc.mean_size
    sum_of_rhoj += rho_j
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

print("*" * 20)
print(f"my_bjs, sum = {sum(my_bjs)} values: {my_bjs }")
print(f"rho_js, sum = {sum_of_rhoj}")

print("*" * 20)

# Verify that the sum of all pij across all job classes is close to 1
# total_p_sum = sum(
#     sum(
#         sij * yij / (jc.arrival_rate / jc.mean_size)
#         for i, (sij, yij) in enumerate(zip(jc.speedup_values, optimal_y[k]))
#     )
#     for k, jc in job_classes.items()
# )
# Initialize total_p_sum
total_p_sum = 0.0

#  accumulate total_p_sum
for k in job_classes:
    jc = job_classes[k]
    for i in range(len(jc.speedup_values)):
        try:
            sij = jc.speedup_values[i]
            yij = optimal_y[k][i]
            total_p_sum += sij * yij * (jc.mean_size / jc.arrival_rate)

        except ZeroDivisionError as zde:
            print(
                f"Warning: {zde} - k = {k}, i= {i}, jc.mean_size = {jc.mean_size}, Skipping this calculation."
            )
        except ValueError as ve:
            print(f"Warning: {ve} Skipping this calculation.")
        except IndexError:
            print(
                f"Warning: Mismatch in data for job class {k}. Skipping this calculation."
            )
        except Exception as e:
            print(f"An unexpected error occurred for job class {k}: {e}")

print(f"\nTotal sum of all pij across job classes: {total_p_sum:.6f}")


# cvxpy see how far you are from your optimal constraints
