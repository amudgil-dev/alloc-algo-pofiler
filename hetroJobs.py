import collections
import random
import numpy as np


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
        )
        self.jobClassMap["B"] = JobClass(
            "B",
            arrival_rate=0.1,
            mean_size=2,
            parallelism=8,
            speedup_function=lambda x: x**0.7,
        )
        self.jobClassMap["C"] = JobClass(
            "C",
            arrival_rate=0.05,
            mean_size=1.5,
            parallelism=10,
            speedup_function=lambda x: x**0.9,
        )
        self.jobClassMap["D"] = JobClass(
            "D",
            arrival_rate=0.15,
            mean_size=0.5,
            parallelism=3,
            speedup_function=lambda x: x**0.6,
        )
        self.jobClassMap["E"] = JobClass(
            "E",
            arrival_rate=0.1,
            mean_size=1.2,
            parallelism=6,
            speedup_function=lambda x: x**0.75,
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
    def __init__(self, name, arrival_rate, mean_size, parallelism, speedup_function):
        self.name = name
        self.arrival_rate = arrival_rate
        self.mean_size = mean_size
        self.parallelism = parallelism
        self.speedup_function = speedup_function
        self.speedup_values = [speedup_function(i) for i in range(1, parallelism + 1)]
        self.yi_stats = [0] * parallelism
        self.arrivalCount = 0
