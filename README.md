## Context on the Project

Unprecedented demands are being placed on compute resources due to HPC jobs such as next-gen machine learning. Distributed systems rely on resource provisioning algorithms to parallelise these jobs across many nodes; however, traditional algorithms are unlikely to perform optimally, resulting in an inefficient and costly waste of resources.

This research aims to:

1. Design the optimal algorithm for parallelisable tasks under real-world workloads.
2. Validate theoretical expectations with results from system simulations.

### Open-Source Simulation Platform

This simulation platform is open-source and intended for researchers and hobbyists in the field of queuing theory and distributed computing. It allows users to profile their own resource allocation algorithms under various workloads and traffic conditions.

**Key Features:**
- Performance profiling for resource allocation algorithms
- graphs for comparison and visualisation
- Customizable workload scenarios through defining various job types

By providing this tool, we aim to foster innovation in resource provisioning algorithms and contribute to more efficient utilization of compute resources in distributed systems.## Context on the Project

# Job Simulation Model
app/models/jump_model.py



## Modelling Incoming Jobs

Jobs are modelled as Poisson processes, characterized by:

- Independence
- Stationarity: The probability of an event occurring in a small time interval is proportional to the length of the interval
- Memorylessness: Events in the next time interval do not depend on the current one

In a Poisson process, interarrival times follow the exponential distribution, which has the memoryless property.

## Mathematical Notation Explained

- λ: Rate of arrival per unit time
- 1/λ: Mean interarrival time
- n: Number of servers
- λ^(n): Rate of arrival per server
- n × λ^(n): scaled Arrival rate of jobs in the system

The system model uses α and β to define how the job arrival rate for a single server λ^(n) scales with the system size n:

λ^(n) = 1 - (β × n^-α)

### Traffic Conditions

We study different traffic conditions:

1. Mean-field regime: α = 0, β ∈ (0, 1)
2. Halfin-Whitt regime: α = 1/2, β > 0
3. Sub-Halfin-Whitt regime: α ∈ (0, 1/2), β > 0
4. Super-Halfin-Whitt regime: α ∈ (1/2, 1), β > 0
5. Super-non-degenerate slowdown (NDS) regime: α ≥ 1

and different inherant size probability distributions:
1. Perato
2. Mixed-Erlang
3. Determinstic
4. Exponential

## Speed-up Function

If a job is allocated to i servers, its execution time decreases by a factor of s(i).
Speed-up function: s = (s(i), i ∈ {0,1,...,d^(n)})

- Linear speed-up case: s(i) = i for all i ∈ [1,d^(n)]
- Sub-linear speed-up case: There exists i ∈ [1,d^(n)] such that s(i) < i

## Jobs Execution Time

The execution time of a job on a single server is an exponential random variable with a unit mean, independent of other jobs' execution times and the arrival process.

Note: We can investigate the effect of different execution time distributions later.

## Queue

If no server is available upon job arrival, the job is blocked/queued (loss).

## Server Allocation Scheme

- A job can run on i ∈ [1,d^n] servers
- A server processes a maximum of 1 job at any given time
- Upon job arrival, if at least 1 server is available, an allocation scheme determines the number of available servers allocated to the job
- Allocated servers remain occupied for the duration of job execution

## p\* Server Allocation Scheme

(Details to be added)

## Questions for Further Investigation

- How to implement the other greedy scheme
- How the sublinear speed-up function is set and incorporated into the model
- Why graphs appear different from final results

## Plots

Expected results:

- Wait time ≈ 0
- Average processing time = 1/d_n (0.1) if d_n is asymptotic, converges to 0

### Simulation Parameters

- Repeat for different values of n: 10, 100, 500, 1000, 1500, 2000
- Compute average wait and average processing time
- Number of jobs should be large, as a function of n. Max jobs = 100n

### Plot 1: Average Wait Time vs. n

- X-axis: Increasing n
- Y-axis: Average wait time
- Should converge

### Plot 2: Average Processing Time vs. n

- Should converge

### Plot 3: Average Wait and Processing Time vs. Normalized Arrival Rate

- Keep n fixed
- Vary λ by changing β: 0.1, 0.2, ..., 0.9
- X-axis: Normalized arrival rate (nλ)
- Y-axis: Average wait time and average processing time
