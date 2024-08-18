import matplotlib.pyplot as plt
import time


# Function to create a single subplot
def create_subplot(ax, data, title, xlabel, ylabel):
    ax.plot(list(data.keys()), list(data.values()), marker="o")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)


def create_plot(data, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(list(data.keys()), list(data.values()), marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()


def plot_jump_model1_results(results, sim):
    if not results:
        print("Error: No results to plot.")
        return

    # Extract data from results
    jobs = []

    times = []
    queue_lengths = []
    jobs_processed = []
    busy_servers = []
    avg_wait_times = []
    avg_processing_times = []

    for stat in results:
        jobs.append(stat.get("jobs", 0))
        times.append(stat.get("time", 0))
        queue_lengths.append(stat.get("queue_length", 0))
        jobs_processed.append(stat.get("jobs_processed", 0))
        busy_servers.append(stat.get("busy_servers", 0))
        avg_wait_times.append(stat.get("avg_wait_time", 0))
        avg_processing_times.append(stat.get("avg_processing_time", 0))

    # Create a figure with subplots
    fig, axs = plt.subplots(3, 2, figsize=(15, 15))
    fig.suptitle("Job Market Simulation Results", fontsize=16)

    # Plot 1: Queue Length over Time
    axs[0, 0].plot(times, queue_lengths)
    axs[0, 0].set_title("Queue Length over Time")
    axs[0, 0].set_xlabel("Time")
    axs[0, 0].set_ylabel("Queue Length")

    # Plot 2: Jobs Processed over Time
    axs[0, 1].plot(times, jobs_processed)
    axs[0, 1].set_title("Jobs Processed over Time")
    axs[0, 1].set_xlabel("Time")
    axs[0, 1].set_ylabel("Jobs Processed")

    # Plot 3: Busy Servers over Time
    axs[1, 0].plot(times, busy_servers)
    axs[1, 0].set_title("Busy Servers over Time")
    axs[1, 0].set_xlabel("Time")
    axs[1, 0].set_ylabel("Number of Busy Servers")

    # Plot 4: Average Wait Time over Time
    axs[1, 1].plot(times, avg_wait_times)
    axs[1, 1].set_title("Average Wait Time over Time")
    axs[1, 1].set_xlabel("Time")
    axs[1, 1].set_ylabel("Average Wait Time")

    # Plot 5: Average Processing Time over Time
    axs[2, 0].plot(times, avg_processing_times)
    axs[2, 0].set_title("Average Processing Time over Time")
    axs[2, 0].set_xlabel("Time")
    axs[2, 0].set_ylabel("Average Processing Time")

    # Plot 6: System Utilization over Time
    if hasattr(sim, "n"):
        utilization = [bs / sim.n for bs in busy_servers]
        axs[2, 1].plot(times, utilization)
        axs[2, 1].set_title("System Utilization over Time")
        axs[2, 1].set_xlabel("Time")
        axs[2, 1].set_ylabel("Utilization")
        axs[2, 1].set_ylim(0, 1)
    else:
        axs[2, 1].text(
            0.5,
            0.5,
            "Utilization data not available",
            horizontalalignment="center",
            verticalalignment="center",
        )

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()
    #
    # save the figure
    file_name = f"simGraphs/jump_model_results_{time.time()}.png"
    plt.savefig(file_name, dpi=300, bbox_inches="tight")
