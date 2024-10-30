import numpy as np
import scipy.stats as stats
from scipy.stats import erlang


class SimStats:

    @staticmethod
    def generate_exponential_job_size(mean):
        if mean <= 0:
            raise ValueError("Mean must be positive.")
        return np.random.exponential(mean)

    @staticmethod
    def generate_deterministic_job_size():
        return 1.0

    @staticmethod
    def generate_mixed_erlang():
        p1, p2 = 0.4, 0.6
        k1, lambda1 = 2, 2  # Erlang with shape 2 and rate 4
        k2, lambda2 = 3, 3  # Erlang with shape 3 and rate 6

        """
        Generates a single job size with a unit mean using a mixture of two Erlang distributions.
        """

        choice = np.random.choice([1, 2], p=[p1, p2])

        if choice == 1:
            job_size = erlang.rvs(k1, scale=1 / lambda1)
        else:
            job_size = erlang.rvs(k2, scale=1 / lambda2)

        return job_size

    # @staticmethod
    # def generate_pareto():
    #     shape = 3 / 2  # Corresponds to the (3y)^3/2 term in the CDF
    #     scale = 1 / 3  # Minimum value for y (threshold)

    #     pareto_rv = stats.pareto(b=shape, scale=scale)

    #     return pareto_rv.rvs()

    @staticmethod
    def generate_pareto():
        shape = 3 / 2  # Corresponds to the (3y)^3/2 term in the CDF
        scale = 1 / 3  # Minimum value for y (threshold)
        return stats.pareto.rvs(b=shape, scale=scale)
