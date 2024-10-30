import numpy as np
import random
import queue

# Define system parameters
n = 100  # number of servers
d_n = 10  # maximum degree of parallelism
alpha = 0.5
beta = 0.1
lambda_n = 1 - beta * n ** (-alpha)  # arrival rate


# Define the speed-up function (amdahl's law)
def speed_up(i, p=0.5):
    return 1 / ((1 - p) + p / i)


# Initialize server states and job queue
servers = [0] * n  # 0 indicates server is idle
job_queue = queue.Queue()


# Simulate job arrivals using Poisson process
def job_arrival(lambda_n):
    return np.random.poisson(lambda_n)


# Server allocation scheme
def allocate_servers(servers, d_n, speed_up_func):
    available_servers = servers.count(0)
    if available_servers == 0:
        return False  # no servers available, job goes to queue
    allocated_servers = min(available_servers, d_n)
    for i in range(allocated_servers):
        servers[servers.index(0)] = 1  # allocate server
    return True  # job is accepted


# Simulation
time_steps = 1000
blocked_jobs = 0
accepted_jobs = 0
queued_jobs = 0

for t in range(time_steps):
    arrivals = job_arrival(lambda_n)
    for _ in range(arrivals):
        if not allocate_servers(servers, d_n, speed_up):
            job_queue.put(1)  # job goes to queue
            queued_jobs += 1
        else:
            accepted_jobs += 1

    # Check the queue and allocate servers if available
    while not job_queue.empty() and servers.count(0) > 0:
        job_queue.get()
        allocate_servers(servers, d_n, speed_up)
        accepted_jobs += 1
        queued_jobs -= 1

    # Update server states (simulate job completion)
    servers = [max(0, s - 1) for s in servers]

# Results
print(f"Total jobs: {blocked_jobs + accepted_jobs + queued_jobs}")
print(f"Blocked jobs: {blocked_jobs}")
print(f"Accepted jobs: {accepted_jobs}")
print(f"Queued jobs: {queued_jobs}")
print(
    f"Blocking probability: {blocked_jobs / (blocked_jobs + accepted_jobs + queued_jobs):.4f}"
)
import numpy as np
from collections import deque

# Define system parameters
n = 100  # Total number of servers
d_n = 10  # Maximum degree of parallelism
queue = deque()  # Initialize an empty queue
queue_limit = np.inf  # Set a limit on the queue size, if needed (infinite for no limit)

# Traffic condition parameters (adjust these according to the regime)
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


# Initialize server states
servers = [0] * n  # 0 indicates server is idle


# Simulate job arrivals and server allocation
def allocate_servers(servers, d_n, speed_up_func):
    available_servers = servers.count(0)
    if available_servers == 0:
        return False  # No servers available, job will go to the queue
    allocated_servers = min(available_servers, d_n)
    for i in range(allocated_servers):
        servers[servers.index(0)] = 1  # Allocate server
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
queue_lengths = []  # To monitor queue length over time

for t in range(time_steps):
    # Simulate job arrival using exponential distribution
    if current_time >= next_arrival_time:
        if not allocate_servers(servers, d_n, speed_up):
            if len(queue) < queue_limit:
                queue.append(current_time)  # Job is queued
        next_arrival_time += np.random.exponential(1 / lambda_n)

    # Update server states (simulate job completion)
    servers = [max(0, s - 1) for s in servers]

    # Process jobs in the queue
    process_queue(servers, queue, d_n, speed_up)

    # Track queue length over time
    queue_lengths.append(len(queue))

    # Increment the current time
    current_time += 1

print("Simulation completed.")
print("Final queue length:", len(queue))
print("Average queue length:", np.mean(queue_lengths))
