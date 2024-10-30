import matplotlib.pyplot as plt

from simdata.sim_parameters import RunParamA

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def start_program():

    distributions = RunParamA.get_distribution()

    # Prepare data
    n_values = [10, 100, 500, 1000, 1500, 2000, 2500, 3000]
    distributions_list = list(distributions.keys())

    # Colors and line styles for the plots
    colors = ["b", "g", "r", "c"]
    markers = ["s", "^", "o", "*"]
    line_styles = ["-", "--", "-.", ":"]

    # Plot wait_n against n
    plt.figure(figsize=(10, 5))
    for i, dist in enumerate(distributions_list):
        wait_n_values = [distributions[dist]["wait_n"].get(n, 0) for n in n_values]
        plt.plot(
            n_values,
            wait_n_values,
            color=colors[i],
            linestyle=line_styles[i],
            label=f"{dist} (wait_n)",
            linewidth=2,
        )

    plt.title("Wait Time (wait_n) vs n", fontsize=14)
    plt.xlabel("n", fontsize=12, weight="bold")
    plt.ylabel("wait_n", fontsize=12, weight="bold")
    plt.legend()
    plt.grid(True)
    plt.tick_params(axis="both", which="major", labelsize=10, width=2)
    plt.tick_params(axis="both", which="minor", width=1)
    plt.show()

    # Plot processing_n against n
    plt.figure(figsize=(10, 5))
    for i, dist in enumerate(distributions_list):
        processing_n_values = [
            distributions[dist]["processing_n"].get(n, 0) for n in n_values
        ]
        plt.plot(
            n_values,
            processing_n_values,
            color=colors[i],
            linestyle=line_styles[i],
            label=f"{dist} (processing_n)",
            linewidth=2,
        )

    plt.title("Processing Time (processing_n) vs n", fontsize=14)
    plt.xlabel("n", fontsize=12, weight="bold")
    plt.ylabel("processing_n", fontsize=12, weight="bold")
    plt.legend()
    plt.grid(True)
    plt.tick_params(axis="both", which="major", labelsize=10, width=2)
    plt.tick_params(axis="both", which="minor", width=1)
    plt.show()
