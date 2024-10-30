import matplotlib.pyplot as plt
from simdata.sim_parameters import RunParamA

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def start_program():

    distributions = RunParamA.get_distribution()

    # Line styles and markers for each distribution
    styles = ["-", "--", "-.", ":"]
    markers = ["s", "^", "o", "*"]
    colors = ["black", "blue", "red", "green"]

    # Plot Average Wait Time vs System Size
    plt.figure(figsize=(10, 6))
    for (name, data), style, marker, color in zip(
        distributions.items(), styles, markers, colors
    ):
        sizes = list(data["wait_n"].keys())
        wait_times = list(data["wait_n"].values())
        plt.plot(
            sizes, wait_times, linestyle=style, marker=marker, color=color, label=name
        )

    plt.xlabel("Number of Servers (n)")
    plt.ylabel("Average Wait Time")
    plt.title("Average Wait Time vs System Size")
    plt.legend(title="Distribution Type")
    plt.grid(True)
    plt.show()

    # Plot Average Processing Time vs System Size
    plt.figure(figsize=(10, 6))
    for (name, data), style, marker, color in zip(
        distributions.items(), styles, markers, colors
    ):
        sizes = list(data["processing_n"].keys())
        processing_times = list(data["processing_n"].values())
        plt.plot(
            sizes,
            processing_times,
            linestyle=style,
            marker=marker,
            color=color,
            label=name,
        )

    plt.xlabel("Number of Servers (n)")
    plt.ylabel("Average Processing Time")
    plt.title("Average Processing Time vs System Size")
    plt.legend(title="Distribution Type")
    plt.grid(True)
    plt.show()
