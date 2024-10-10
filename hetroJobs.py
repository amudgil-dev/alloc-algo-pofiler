import collections
import random
import numpy as np
import numpy as np
from scipy.stats import erlang


class JobClassManager:
    def __init__(self):
        # self.jobClassMap = collections.defaultdict(JobClass)
        self.jobClassMap = {}

        self.initJobClasses()
        self.totalArrivalRate = self.getTotalArrivalRate()

    def getTotalArrivalRate(self):
        arrivalRate = 0
        for v in self.jobClassMap.values():
            arrivalRate += v.arrival_rate
        return arrivalRate

    def initJobClasses(self):
        self.jobClassMap["A"] = JobClass(
            "A",
            arrival_rate=0.1,
            mean_size=1,
            parallelism=5,
            speedup_function=lambda x: x**0.8,
            # generate_job_size_function=lambda: generate_mixed_erlang(),
            # generate_job_size_function=lambda: generate_exponential_job_size(1),
            # generate_job_size_function=lambda: generate_deterministic_job_size(),
            generate_job_size_function=lambda: generate_perato(),
        )
        self.jobClassMap["B"] = JobClass(
            "B",
            arrival_rate=0.1,
            mean_size=2,
            parallelism=8,
            speedup_function=lambda x: x**0.7,
            # generate_job_size_function=lambda: generate_mixed_erlang(),
            # generate_job_size_function=lambda: generate_exponential_job_size(2),
            # generate_job_size_function=lambda: generate_deterministic_job_size(),
            generate_job_size_function=lambda: generate_perato(),
        )
        self.jobClassMap["C"] = JobClass(
            "C",
            arrival_rate=0.05,
            mean_size=1.5,
            parallelism=10,
            speedup_function=lambda x: x**0.9,
            # generate_job_size_function=lambda: generate_mixed_erlang(),
            # generate_job_size_function=lambda: generate_exponential_job_size(1.5),
            # generate_job_size_function=lambda: generate_deterministic_job_size(),
            generate_job_size_function=lambda: generate_perato(),
        )
        self.jobClassMap["D"] = JobClass(
            "D",
            arrival_rate=0.15,
            mean_size=0.5,
            parallelism=3,
            speedup_function=lambda x: x**0.6,
            # generate_job_size_function=lambda: generate_mixed_erlang(),
            # generate_job_size_function=lambda: generate_exponential_job_size(0.5),
            # generate_job_size_function=lambda: generate_deterministic_job_size(),
            generate_job_size_function=lambda: generate_perato(),
        )
        self.jobClassMap["E"] = JobClass(
            "E",
            arrival_rate=0.1,
            mean_size=1.2,
            parallelism=6,
            speedup_function=lambda x: x**0.75,
            # generate_job_size_function=lambda: generate_mixed_erlang(),
            # generate_job_size_function=lambda: generate_exponential_job_size(1.2),
            # generate_job_size_function=lambda: generate_deterministic_job_size(),
            generate_job_size_function=lambda: generate_perato(),
        )

    def determineJobClass(self):
        random_num = random.uniform(0, 1)
        for k, v in self.jobClassMap.items():
            random_num -= v.arrival_rate * (1 / self.totalArrivalRate)
            if random_num <= 0:
                # print("in hetro jobs returning class name", k)
                return k

    def get_jobClass_yi_stats(self):
        stats = {}
        for name, job_class in self.jobClassMap.items():
            if job_class.arrivalCount > 0:
                stats[name] = np.divide(job_class.yi_stats, job_class.arrivalCount)
            else:
                stats[name] = np.zeros_like(job_class.yi_stats)
        return stats


class JobClass:

    def __init__(
        self,
        name,
        arrival_rate,
        mean_size,
        parallelism,
        speedup_function,
        generate_job_size_function,
    ):
        self.name = name
        self.arrival_rate = arrival_rate
        self.mean_size = mean_size
        self.parallelism = parallelism
        self.speedup_function = speedup_function
        self.speedup_values = [speedup_function(i) for i in range(1, parallelism + 1)]
        self.yi_stats = [0] * parallelism
        self.arrivalCount = 0
        self.generate_job_size_function = generate_job_size_function


def generate_exponential_job_size(mean):
    return np.random.exponential(mean)


def generate_deterministic_job_size():
    return 1.0


# Define Erlang distribution parameters for the two components


def generate_mixed_erlang():
    p1, p2 = 0.4, 0.6
    k1, lambda1 = 2, 2  # Erlang with shape 2 and rate 4
    k2, lambda2 = 3, 3  # Erlang with shape 3 and rate 6
    # 2 exp w unit mean- sample w p1 & p2

    """
    Generates a single job size with a unit mean using a mixture of two Erlang distributions.
    """

    # Draw from a Bernoulli distribution to choose which Erlang component to sample from
    choice = np.random.choice([1, 2], p=[p1, p2])

    # Generate a single sample based on the choice
    if choice == 1:
        job_size = erlang.rvs(k1, scale=1 / lambda1)
    else:
        job_size = erlang.rvs(k2, scale=1 / lambda2)

    return job_size


import numpy as np
import scipy.stats as stats


def generate_perato():
    # Parameters from the given CDF
    shape = 3 / 2  # Corresponds to the (3y)^3/2 term in the CDF
    scale = 1 / 3  # Minimum value for y (threshold)

    # Generate a random variable from the Pareto distribution
    pareto_rv = stats.pareto(b=shape, scale=scale)

    # Return a random job size
    return pareto_rv.rvs()
