from collections import namedtuple
import sys


# # Custom class
# class Job:
#     def __init__(self, id, title):
#         self.id = id
#         self.title = title


# # Named tuple
# JobTuple = namedtuple("JobTuple", ["id", "title"])

# # Memory usage
# print(f"Custom class: {sys.getsizeof(Job(1, 'Engineer'))} bytes")
# print(f"Named tuple: {sys.getsizeof(JobTuple(1, 'Engineer'))} bytes")


from collections import namedtuple
import sys
import tracemalloc


# Custom class
class Job:
    def __init__(self, id, title):
        self.id = id
        self.title = title


# Named tuple
JobTuple = namedtuple("JobTuple", ["id", "title"])


def measure_memory(create_func, n=1_000_000):
    tracemalloc.start()
    objects = [create_func(i, f"Job {i}") for i in range(n)]
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024 / 1024  # Convert to MB


class_memory = measure_memory(lambda id, title: Job(id, title))
tuple_memory = measure_memory(lambda id, title: JobTuple(id, title))

print(f"Memory for 1M class instances: {class_memory:.2f} MB")
print(f"Memory for 1M named tuple instances: {tuple_memory:.2f} MB")
