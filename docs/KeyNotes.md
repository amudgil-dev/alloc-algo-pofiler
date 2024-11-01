Modelling incoming jobs:
    Job events are modelled as poisson processes: independance, stationarity (probability of event occuringin small time interval is proportional to the length of the interval), memorylessness (events of the next time interval do not depend on this one)

    in a poisson process, interarrival times follow the exponential distribution- it has memoryless property

job arrival times:
    𝜆 is rate of arrival/unit time, 1/𝜆 is mean interarrival time

    n is number of servers, λ^(n) is the rate of arrival per server so n x λ^(n) is arrival rate of jobs

    α and 𝛽 in your system model define how the job arrival rate for single server 𝜆^(𝑛) scales with the system size 𝑛.

    𝜆^(𝑛) = 1 -  (𝛽 x n^-α)


    we want to study under different traffic conditions:
    1)the mean-field regime which corresponds to 𝛼 = 0, 𝛽 ∈ (0, 1)
    2)the Halfin-Whitt regime which corresponds to 𝛼 = 1/2, 𝛽 > 0
    3)the sub-Halfin-Whitt (resp. super-Halfin-Whitt) regime corresponding to 𝛼 ∈ (0, 1/2), 𝛽 > 0 (resp. 𝛼 ∈ (1/2, 1), 𝛽 > 0)
    4)the super-non-degenerate slow- down (NDS) regime corresponding to 𝛼 ≥ 1.




speed up function:

    if a job is allocated to i servers,its execution time decreases by factor of s(i). speed up function: s= (s(i), i ∈ {0,1,...,d^(n)})

    linear speed-up case: s(i) = i for all i ∈ [1,d^(n)]
    sub-linear speed-up case: there exists i ∈ [1,d^(n)] such that s(i) < i

jobs execution time:
    execution time of job on a single server is an exponential random variable with a unit mean ,independant of other jobs' execution times and the arrival process

    CAN INVESTIGATE EFFECT OF DIFFERENT EXECUTION TIME DISTRIBUTIONS LATER

queue:
    upon job arrival if no server is found available, the job is blocked/queued = loss.

server allocation scheme:
    a job can run on i ∈ [1,d^n] servers, a server processes max 1 job at any given time

    upon job arrival if atleast 1 server is available an allocation scheme is used to determine the number of available servers allocated to the job
    allocated server will remain occupied as long as the job executes


p* server allocation scheme:


qs for arpan:
- how to try the other greedy scheme
- how the sublinear speed up function is set & how to incorporate it into my model
- why graphs appear different to final results



plots;
- expect: wait time = near 0, ave processing time = 1/d_n (0.1) if d_n is asymptotic, converges to 0

- repeat for different values of n: 10-2000: 10, 100, 500, 1000, 1500, 2000
- compute ave wait & ave processing time

- number of jobs should be large, as a function of n. max jobs = 100n

plot 1: ave wait time as a function of n
- increasing n on x axis, ave wait time of y axis.
- should converge

plot 2: ave processing time as a function of n
- should converge

plot 3: ave wait & processing as a function of n 𝜆, or a function of 𝛽
- normalised arrival rate by size of system- keep n fixed, vary 𝜆 by changing 𝛽 0.1,0.2...0.9

