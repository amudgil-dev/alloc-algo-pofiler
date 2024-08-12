import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Define system parameters
n = 10000  # Total number of servers
d_n = 100  # Maximum degree of parallelism
queue = deque()  # Initialize an empty queue
queue_limit = np.inf  # Set a limit on the queue size, if needed (infinite for no limit)

# Traffic condition parameters
alpha = 0.5  # Example value, change this according to the regime
beta = 0.9  # Example value, change this according to the regime


# Define the arrival rate function based on the system size n, alpha, and beta
def arrival_rate(n, alpha, beta):
    return 1 - beta * n ** (-alpha)


# Compute the arrival rate for the current system size
lambda_n = arrival_rate(n, alpha, beta)


# Define the speed-up function
def speed_up(i, p=0.5):
    return 1 / ((1 - p) + p / i)


# Initialize server states (0 means idle, positive values indicate remaining time)
servers = [0] * n


# Simulate job arrivals and server allocation
def allocate_servers(servers, d_n, speed_up_func):
    available_servers = servers.count(0)
    if available_servers == 0:
        return False  # No servers available, job will go to the queue
    allocated_servers = min(available_servers, d_n)
    execution_time = int(10 * speed_up(allocated_servers))  # Example execution time
    for i in range(allocated_servers):
        servers[servers.index(0)] = (
            execution_time  # Allocate server with execution time
        )
    return True  # Job is accepted


# Process the queue when servers are available
def process_queue(servers, queue, d_n, speed_up_func):
    while queue and servers.count(0) >= d_n:
        queue.popleft()  # Remove the job from the queue
        allocate_servers(servers, d_n, speed_up_func)


# Simulation loop
time_steps = 1000
current_time = 0
next_arrival_time = np.random.exponential(1 / lambda_n)

# Metrics to track
queue_lengths = []
busy_servers = []
jobs_arrived = []
jobs_completed = []

jobs_arrival_count = 0
jobs_completion_count = 0

for t in range(time_steps):
    # Simulate job arrival using exponential distribution
    if current_time >= next_arrival_time:
        jobs_arrival_count += 1
        if not allocate_servers(servers, d_n, speed_up):
            if len(queue) < queue_limit:
                queue.append(current_time)  # Job is queued
        next_arrival_time += np.random.exponential(1 / lambda_n)

    # Update server states (simulate job completion)
    for i in range(n):
        if servers[i] > 0:
            servers[i] -= 1  # Decrease the remaining time for each busy server
            if servers[i] == 0:
                jobs_completion_count += 1  # Job completed, increase distinct job count

    # Process jobs in the queue
    process_queue(servers, queue, d_n, speed_up)

    # Record metrics at this time step
    queue_lengths.append(len(queue))
    busy_servers.append(n - servers.count(0))
    jobs_arrived.append(jobs_arrival_count)
    jobs_completed.append(jobs_completion_count)

    # Increment the current time
    current_time += 1

# Plotting the results
time = np.arange(time_steps)

plt.figure(figsize=(14, 10))

# Plot queue length over time
plt.subplot(2, 2, 1)
plt.plot(time, queue_lengths, label="Queue Length")
plt.xlabel("Time Steps")
plt.ylabel("Queue Length")
plt.title("Queue Length Over Time")
plt.grid(True)

# Plot busy servers over time
plt.subplot(2, 2, 2)
plt.plot(time, busy_servers, label="Busy Servers", color="orange")
plt.xlabel("Time Steps")
plt.ylabel("Number of Busy Servers")
plt.title("Busy Servers Over Time")
plt.grid(True)

# Plot cumulative jobs arrived over time
plt.subplot(2, 2, 3)
plt.plot(time, jobs_arrived, label="Jobs Arrived", color="green")
plt.xlabel("Time Steps")
plt.ylabel("Cumulative Jobs Arrived")
plt.title("Jobs Arrived Over Time")
plt.grid(True)

# Plot cumulative jobs completed over time
plt.subplot(2, 2, 4)
plt.plot(time, jobs_completed, label="Jobs Completed", color="red")
plt.xlabel("Time Steps")
plt.ylabel("Cumulative Jobs Completed")
plt.title("Jobs Completed Over Time")
plt.grid(True)

plt.tight_layout()
plt.show()
