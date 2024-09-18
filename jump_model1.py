import numpy as np
import heapq
from collections import deque, namedtuple
from pallocationStrat import getOptimalServerNum, init_Pstar
import math
from equi_no_repacking import get_equi_no_repacking_servers


"""
jump_model1 context:
- self.events is a minheap for event scheduling & time management: allows sim to jump to next event rather than incrementing time step by step
- minheap removes event with earliest time and model processes it

"""


# model job characteristics with named tuple
Job = namedtuple(
    "Job",
    [
        "arrival_time",
        "execution_time",
        "allocated_servers",
        "start_time",
        "finish_time",
    ],
)


class JobMarketSim:
    def __init__(self, n, beta, alpha, d_n, max_jobs):
        self.n = n  # number of servers
        self.beta = beta
        self.alpha = alpha
        self.d_n = d_n  # max degree of parellelism
        self.max_jobs = max_jobs

        # calculate arrival rate of jobs
        self.arrival_rate = self.n * (1 - (self.beta * self.n ** (-self.alpha)))

        self.time = 0  # to simulatee time units passing
        self.servers = [0] * n  # keep track of the time a server is occupied untill
        self.queue = deque()
        self.events = []  # minheap for event scheduling

        # monitoring stats
        self.jobs_arrived = 0
        self.jobs_processed = 0
        self.total_wait_time = 0
        self.total_processing_time = 0

    # constructor with max jobs as a function of n
    def __init__(self, n, beta, alpha, d_n):
        self.n = n  # number of servers
        self.beta = beta
        self.alpha = alpha
        self.d_n = d_n  # max degree of parellelism
        self.max_jobs = n * 100

        self.total_jobs_in_system = 0
        self.n_yt_denomiator = 0
        self.n_yt = 0

        # calculate arrival rate of jobs
        self.arrival_rate = self.n * (1 - (self.beta * self.n ** (-self.alpha)))
        # self.arrival_rate = 0.5 * self.n

        self.time = 0  # to simulatee time units passing
        self.servers = [0] * n  # keep track of the time a server is occupied untill
        self.queue = deque()
        self.events = []  # minheap for event scheduling
        print(
            f"arrival rate = {self.arrival_rate} / n = {self.n} = {self.arrival_rate / self.n}"
        )

        self.p1 = init_Pstar(
            self.d_n, (self.arrival_rate / self.n), self.get_speedup_factor
        )  # for p* allocation scheme
        # monitoring stats
        self.jobs_arrived = 0
        self.jobs_processed = 0
        self.total_wait_time = 0
        self.total_processing_time = 0

    def generate_interarrival_time(self):
        return np.random.exponential(1 / self.arrival_rate)

    def generate_execution_time(self):
        return np.random.exponential(1)  # job exe time is ave 1 unit

    """
    linear speed up function
    """

    def get_speedup_factor(self, allocated_servers):
        # return allocated_servers**0.25  # sub-linear
        return allocated_servers  # linear

    """
    simple greedy allocation scheme:
    upon job arrival, calculate number of free servers and return the maximum possible servers the job can be allocated to
    """

    def allocate_servers(self):
        # calculate the number of free servers
        available_servers = sum(
            1 for server_time in self.servers if server_time < self.time
        )
        # optimal = getOptimalServerNum(self.p1)

        optimal = get_equi_no_repacking_servers(self.n_yt)
        # print("optimal ", optimal)

        # return min(available_servers, self.d_n) # greedy allocation scheme
        return min(available_servers, optimal, self.d_n)  # P* allocation scheme

    """
    - calculate free servers
    - queue job if no free servers
    - else allocate the jobs as per the allocation scheme and - update the time each server is busy until.
    - log stats
    """

    def process_job(self, job):
        allocated_servers = self.allocate_servers()

        if allocated_servers == 0:
            self.queue.append(job)

        else:
            parallelised_exe_time = job.execution_time / self.get_speedup_factor(
                allocated_servers
            )
            job_start_time = self.time
            job_finish_time = self.time + parallelised_exe_time

            # update server states
            allocated = 0
            for i, server_time in enumerate(self.servers):
                if server_time <= self.time and allocated < allocated_servers:
                    self.servers[i] = job_finish_time
                    allocated += 1

            heapq.heappush(self.events, (job_finish_time, "finish"))

            # update stats
            self.jobs_processed += 1
            self.total_wait_time += job_start_time - job.arrival_time
            self.total_processing_time += job_finish_time - job_start_time

    def run_simulation(self):
        next_arrival = self.time + self.generate_interarrival_time()
        heapq.heappush(self.events, (next_arrival, "arrival"))

        stats = []

        """
        main sim loop for processing events
        - for arrivals: process arrival then schedule next. When job starts processing its completion is scheduled
        - for finish: process next job in queue

        """
        while self.events and self.jobs_arrived < self.max_jobs:
            self.time, event_type = heapq.heappop(self.events)

            if event_type == "arrival":
                self.total_jobs_in_system += 1
                self.jobs_arrived += 1
                # create new Job tuple
                new_job = Job(self.time, self.generate_execution_time(), 0, None, None)

                # if no queue, reset n_yt
                if len(self.queue) == 0:
                    self.n_yt_denomiator = self.total_jobs_in_system
                else:
                    self.n_yt_denomiator += 1

                self.n_yt = self.n / self.n_yt_denomiator

                self.process_job(new_job)

                if self.jobs_arrived < self.max_jobs:
                    next_arrival = self.time + self.generate_interarrival_time()
                    heapq.heappush(self.events, (next_arrival, "arrival"))

            # if jobs finishes, means servers are free so can process next
            elif event_type == "finish":
                self.total_jobs_in_system -= 1
                if self.queue:
                    self.process_job(self.queue.popleft())

            # collect stats every 10 jobs
            # if (
            #     self.jobs_arrived % 10 == 0 and self.jobs_processed > 0
            # ):  # catch divide by 0 case
            # busy_servers = sum(
            #     1 for server_time in self.servers if server_time > self.time
            # )

            # stats.append(
            #     {
            #         "jobs": self.jobs_arrived,
            #         "time": self.time,
            #         "queue_length": len(self.queue),
            #         "jobs_processed": self.jobs_processed,
            #         "busy_servers": busy_servers,
            #         "ave_wait_time": self.total_wait_time / self.jobs_processed,
            #         "ave_processing_time": self.total_processing_time
            #         / self.jobs_processed,
            #     }
            # )

        return stats
