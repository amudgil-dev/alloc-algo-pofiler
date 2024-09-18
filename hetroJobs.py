import numpy as np
from Math import random
from jump_model1 import Job
import time

job_classes = {
    "class_1": {
        "execution_time": lambda: np.random.exponential(1),
        "speedup": lambda x: x**0.5,
    },
    "class_2": {
        "execution_time": lambda: np.random.exponential(2),
        "speedup": lambda x: np.log(x + 1),
    },
    "class_3": {
        "execution_time": lambda: np.random.exponential(3),
        "speedup": lambda x: np.log(x + 1),
    },
    "class_4": {
        "execution_time": lambda: np.random.exponential(4),
        "speedup": lambda x: np.log(x + 1),
    },
}


def generate_job():
    job_class = random.choice(list(job_classes.keys()))  # Randomly choose a job class
    execution_time = job_classes[job_class]["execution_time"]()
    return Job(
        arrival_time=current_time, execution_time=execution_time, job_class=job_class
    )


def allocate_servers(job):
    job_class = job.job_class
    speedup_function = job_classes[job_class]["speedup"]
    available_servers = sum(
        1 for server_time in self.servers if server_time < self.time
    )
    optimal_servers = min(
        available_servers, self.d_n
    )  # Example: use a simple greedy scheme
    return min(available_servers, optimal_servers)
