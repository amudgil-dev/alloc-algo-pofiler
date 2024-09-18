from jump_model1 import JobMarketSim
from db_manager import db_dump, db_clear
import time
from jump_model1_graphs import plot_jump_model1_results, create_plot, create_subplot
from pprint import pprint
import matplotlib.pyplot as plt


vary_n = [10, 100, 500, 1000, 1500, 2000, 2500, 3000]
vary_beta = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

wait_n = {}
processing_n = {}
wait_arrival = {}
processing_arrival = {}

for n in vary_n:

    myparams = {"n": n, "beta": 0.3, "alpha": 0, "d_n": 10}

    print(f"sim starting: {time.time()}")
    sim = JobMarketSim(**myparams)

    sim.run_simulation()
    print(f"sim over: {time.time()}")

    print(f"\nFinal stats:")
    print(f"Total jobs arrived: {sim.jobs_arrived}")
    print(f"Total jobs processed: {sim.jobs_processed}")
    print(f"Jobs in queue: {len(sim.queue)}")
    print(f"Average wait time: {sim.total_wait_time / sim.jobs_processed:.2f}")
    print(
        f"Average processing time: {sim.total_processing_time / sim.jobs_processed:.2f}"
    )
    wait_n[n] = sim.total_wait_time / sim.jobs_processed
    processing_n[n] = sim.total_processing_time / sim.jobs_processed

for beta in vary_beta:
    myparams = {"n": 1000, "beta": beta, "alpha": 0, "d_n": 10}

    print(f"sim starting: {time.time()}")
    sim = JobMarketSim(**myparams)

    sim.run_simulation()
    print(f"sim over: {time.time()}")
    print(f"\nFinal stats:")
    print(f"Total jobs arrived: {sim.jobs_arrived}")
    print(f"Total jobs processed: {sim.jobs_processed}")
    print(f"Jobs in queue: {len(sim.queue)}")
    print(f"Average wait time: {sim.total_wait_time / sim.jobs_processed:.2f}")
    print(
        f"Average processing time: {sim.total_processing_time / sim.jobs_processed:.2f}"
    )
    wait_arrival[sim.arrival_rate] = sim.total_wait_time / sim.jobs_processed
    processing_arrival[sim.arrival_rate] = (
        sim.total_processing_time / sim.jobs_processed
    )


# Create a figure with 2x2 subplots
fig, axs = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Performance Metrics", fontsize=16)

# Create individual subplots for each dictionary
create_subplot(
    axs[0, 0],
    wait_n,
    "Average Wait Time vs Number of Servers",
    "Number of Servers (n)",
    "Average Wait Time",
)
create_subplot(
    axs[0, 1],
    processing_n,
    "Average Processing Time vs Number of Servers",
    "Number of Servers (n)",
    "Average Processing Time",
)
create_subplot(
    axs[1, 0],
    wait_arrival,
    "Average Wait Time vs Arrival Rate",
    "Normalised Arrival Rate (nλ)",
    "Average Wait Time",
)
create_subplot(
    axs[1, 1],
    processing_arrival,
    "Average Processing Time vs Arrival Rate",
    "Normalised Arrival Rate (nλ)",
    "Average Processing Time",
)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig("equi_no_repack_lin_speedup.png", dpi=300)
plt.close()

print(
    "All plots have been generated and saved in a single image: performance_metrics.png"
)

# print(wait_n)
# create_plot(
#     wait_n,
#     "Average Wait Time vs Number of Servers",
#     "Number of Servers (n)",
#     "Average Wait Time",
#     "wait_time_vs_n.png",
# )

# print(processing_n)
# create_plot(
#     processing_n,
#     "Average Processing Time vs Number of Servers",
#     "Number of Servers (n)",
#     "Average Processing Time",
#     "processing_time_vs_n.png",
# )


# print(wait_arrival)
# create_plot(
#     wait_arrival,
#     "Average Wait Time vs Arrival Rate",
#     "Normalised Arrival Rate (nλ)",
#     "Average Wait Time",
#     "wait_time_vs_arrival_rate.png",
# )
# print(processing_arrival)
# create_plot(
#     processing_arrival,
#     "Average Processing Time vs Arrival Rate",
#     "Normalised Arrival Rate (nλ)",
#     "Average Processing Time",
#     "processing_time_vs_arrival.png",
# )

# print("All plots have been generated and saved.")

# # plotting results
# plot_jump_model1_results(results, sim)

# db_clear()
# db_dump(myparams, results)
# print("added to db")
