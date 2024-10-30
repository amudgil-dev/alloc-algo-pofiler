import numpy as np
import heapq
from collections import deque, namedtuple
from pallocationStrat import getOptimalServerNum, init_Pstar
import math
from equi_no_repacking import get_equi_no_repacking_servers
from hetroJobs import JobClassManager

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
        "job_class",
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

        self.time = 0  # to simulate time units passing
        self.servers = [0] * n  # keep track of the time a server is occupied untill
        self.queue = deque()
        self.events = []  # minheap for event scheduling

        # monitoring stats
        self.jobs_arrived = 0
        self.jobs_processed = 0
        self.total_wait_time = 0
        self.total_processing_time = 0

    # constructor with max jobs as a function of n
    # now with multi job classes
    def __init__(self, n, beta, alpha, d_n):
        # instantiate the job classes
        self.jobClassManager = JobClassManager()
        self.n = n  # number of servers
        self.beta = beta
        self.alpha = alpha
        self.d_n = d_n  # max degree of parellelism
        self.max_jobs = n * 100

        self.total_jobs_in_system = 0
        self.n_yt_denomiator = 0
        self.n_yt = 0

        # calculate arrival rate of jobs

        # self.arrival_rate = self.n * (1 - (self.beta * self.n ** (-self.alpha)))
        # self.arrival_rate = 0.5 * self.n

        # total arrival rate is sum of arri rate of the l job classes
        self.arrival_rate = self.n * self.jobClassManager.totalArrivalRate

        self.time = 0  # to simulatee stime units passing
        self.servers = [0] * n  # keep track of the time a server is occupied untill
        self.queue = deque()
        self.events = []  # minheap for event scheduling
        print(
            f"arrival rate = {self.arrival_rate} / n = {self.n} = {self.arrival_rate / self.n}"
        )

        # self.p1 = init_Pstar(
        #     self.d_n, (self.arrival_rate / self.n), self.get_speedup_factor
        # )  # for p* allocation scheme

        # monitoring stats
        self.jobs_arrived = 0
        self.jobs_processed = 0
        self.total_wait_time = 0
        self.total_processing_time = 0

    def generate_interarrival_time(self):
        return np.random.exponential(1 / self.arrival_rate)

    # def generate_execution_time(self):
    #     return np.random.exponential(1)  # job exe time is ave 1 unit

    # for hetro class case
    def generate_execution_time(self, jobClassName):
        # print(" in generate_exe_time", jobClassName)
        jobClass = self.jobClassManager.jobClassMap[jobClassName]
        # return np.random.exponential(jobClass.mean_size)  # job exe time is ave 1 unit
        return jobClass.generate_job_size_function()  # job exe time is ave 1 unit

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
        # return min(available_servers, optimal, self.d_n)  # P* allocation scheme
        return min(available_servers, optimal)  # P* allocation scheme

    """
    - calculate free servers
    - queue job if no free servers
    - else allocate the jobs as per the allocation scheme and - update the time each server is busy until.
    - log stats
    """

    def alloc_servers_pstar(self, jobClass_Obj):
        # print(f"in alloc servers pstar {jobClass_Obj}")

        # Determine the number of servers to allocate based on the job class strategy
        if jobClass_Obj.pstar_alloc_strategy["type"] == "probabilistic":
            probs = jobClass_Obj.pstar_alloc_strategy["probs"]
            allocated_servers = np.random.choice(
                list(probs.keys()), p=list(probs.values())
            )
        elif jobClass_Obj.pstar_alloc_strategy["type"] == "fixed":
            allocated_servers = jobClass_Obj.pstar_alloc_strategy["servers"]
        return allocated_servers

    def process_job(self, job):
        jobClass = self.jobClassManager.jobClassMap[job.job_class]
        # allocated_servers = min(self.allocate_servers(), jobClass.parallelism)
        available_servers = sum(
            1 for server_time in self.servers if server_time < self.time
        )
        allocated_servers = min(
            self.alloc_servers_pstar(jobClass), jobClass.parallelism, available_servers
        )

        if allocated_servers == 0:
            self.queue.append(job)

        else:
            # parallelised_exe_time = job.execution_time / self.get_speedup_factor(
            #     allocated_servers
            # )

            self.jobClassManager.jobClassMap[job.job_class].yi_stats[
                allocated_servers - 1
            ] += 1

            parallelised_exe_time = job.execution_time / jobClass.speedup_function(
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
                classForNewJob = self.jobClassManager.determineJobClass()
                self.jobClassManager.jobClassMap[classForNewJob].arrivalCount += 1
                # print("under classForNewJob", classForNewJob)
                # new_job = Job(
                #     self.time, self.generate_execution_time(), 0, None, None, classForNewJob
                # )

                new_job = Job(
                    self.time,
                    self.generate_execution_time(classForNewJob),
                    0,
                    None,
                    None,
                    classForNewJob,
                )

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

        return self.jobClassManager.get_jobClass_yi_stats()
