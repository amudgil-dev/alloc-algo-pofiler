import numpy as np
import random

# Define system parameters
n = 100  # number of servers
d_n = 10  # maximum degree of parallelism
alpha = 0.5
beta = 0.1
lambda_n = 1 - beta * n ** (-alpha)  # arrival rate


# Define the speed-up function
def speed_up(i, p=0.5):
    return 1 / ((1 - p) + p / i)


# Initialize server states
servers = [0] * n  # 0 indicates server is idle


# Simulate job arrivals using Poisson process
def job_arrival(lambda_n):
    return np.random.poisson(lambda_n)


# Server allocation scheme
def allocate_servers(servers, d_n, speed_up_func):
    available_servers = servers.count(0)
    if available_servers == 0:
        return False  # job is blocked
    allocated_servers = min(available_servers, d_n)
    for i in range(allocated_servers):
        servers[servers.index(0)] = 1  # allocate server
    return True  # job is accepted


# Simulation
time_steps = 1000
blocked_jobs = 0
accepted_jobs = 0

for t in range(time_steps):
    arrivals = job_arrival(lambda_n)
    for _ in range(arrivals):
        if not allocate_servers(servers, d_n, speed_up):
            blocked_jobs += 1
        else:
            accepted_jobs += 1
    # Update server states (simulate job completion)
    servers = [max(0, s - 1) for s in servers]

# Results
print(f"Total jobs: {blocked_jobs + accepted_jobs}")
print(f"Blocked jobs: {blocked_jobs}")
print(f"Accepted jobs: {accepted_jobs}")
print(f"Blocking probability: {blocked_jobs / (blocked_jobs + accepted_jobs):.4f}")
