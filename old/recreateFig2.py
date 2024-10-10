import numpy as np
import matplotlib.pyplot as plt

# from scipy import stats
# from scipy.stats import poisson


class ServerAllocationSimulator:
    def __init__(self, n, d_n, alpha, beta, speed_up_func, T):
        self.n = n
        self.d_n = d_n
        self.alpha = alpha
        self.beta = beta
        self.lambda_n = 1 - beta * n ** (-alpha)
        self.speed_up = speed_up_func
        self.T = T
        self.servers = [0] * n
        self.state = [0] * (d_n + 1)
        self.blocked_jobs = 0
        self.total_jobs = 0
        self.total_execution_time = 0

    def allocate_servers(self, p_star):
        available_servers = self.servers.count(0)
        if available_servers == 0:
            self.blocked_jobs += 1
            return False

        allocated_servers = np.random.choice(range(1, self.d_n + 1), p=p_star)
        allocated_servers = min(allocated_servers, available_servers)

        for i in range(allocated_servers):
            self.servers[self.servers.index(0)] = 1
        self.state[allocated_servers] += 1
        self.total_execution_time += 1 / self.speed_up(allocated_servers)
        return True

    def complete_job(self, i):
        if self.state[i] > 0:
            self.state[i] -= 1
            for _ in range(i):
                self.servers[self.servers.index(1)] = 0

    def run_simulation(self, p_star):
        current_time = 0
        next_arrival = np.random.exponential(1 / (self.n * self.lambda_n))

        while current_time < self.T:
            if current_time >= next_arrival:
                self.total_jobs += 1
                self.allocate_servers(p_star)
                next_arrival += np.random.exponential(1 / (self.n * self.lambda_n))

            for i in range(1, self.d_n + 1):
                if self.state[i] > 0:
                    if np.random.random() < self.speed_up(i) / self.n:
                        self.complete_job(i)

            current_time += 1 / self.n

    def get_results(self):
        blocking_prob = self.blocked_jobs / self.total_jobs
        avg_execution_time = self.total_execution_time / (
            self.total_jobs - self.blocked_jobs
        )
        return blocking_prob, avg_execution_time


def speed_up(i, p=0.9):
    return 1 / ((1 - p) + p / i)


# Simulation parameters
d_n = 10
beta = 0.1
T = 10000

# Define p* (optimal probability distribution)
p_star = [0.1, 0.2, 0.3, 0.2, 0.1, 0.05, 0.05, 0, 0, 0]

# Vary alpha and system size
alpha_values = np.linspace(0, 1, 20)
n_values = [100, 500, 1000]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

for n in n_values:
    blocking_probs = []
    avg_execution_times = []

    for alpha in alpha_values:
        sim = ServerAllocationSimulator(n, d_n, alpha, beta, speed_up, T)
        sim.run_simulation(p_star)
        blocking_prob, avg_execution_time = sim.get_results()
        blocking_probs.append(blocking_prob)
        avg_execution_times.append(avg_execution_time)

    ax1.plot(alpha_values, blocking_probs, marker="o", label=f"n = {n}")
    ax2.plot(alpha_values, avg_execution_times, marker="o", label=f"n = {n}")

ax1.set_xlabel("α")
ax1.set_ylabel("Blocking Probability")
ax1.set_yscale("log")
ax1.legend()
ax1.grid(True)

ax2.set_xlabel("α")
ax2.set_ylabel("Average Execution Time")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
