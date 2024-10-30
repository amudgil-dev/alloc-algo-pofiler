"""
This module combines simulation and plotting functionality for a job market simulation.
It runs simulations with varying parameters, saves results, and generates plots.
"""

import os
import json
import time
import matplotlib.pyplot as plt
from app.utils.util import Util
from app.models.jump_model import JobMarketSim
from app.models.jump_model_graphs import create_subplot
from config import Config

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def ensure_directory_exists(directory):
    """
    Ensure that the specified directory exists, creating it if necessary.

    Args:
        directory (str): The path of the directory to check/create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_to_json(data, prefix):
    """
    Save data to a JSON file with a unique filename.

    Args:
        data (dict): The data to be saved.
        prefix (str): Prefix for the filename.

    Returns:
        str: The path of the saved file.
    """
    filename = Util.generate_filename(prefix, "json")
    file_path = os.path.join(Config.RESULTS_FOLDER, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return file_path


def save_to_txt(content, prefix):
    """
    Save content to a text file with a unique filename.

    Args:
        content (str): The content to be saved.
        prefix (str): Prefix for the filename.

    Returns:
        str: The path of the saved file.
    """
    filename = Util.generate_filename(prefix, "txt")
    file_path = os.path.join(Config.RESULTS_FOLDER, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


def run_simulation_and_store_results(param_name, vary_values, simulation_params):
    """
    Run simulations for varying parameter values and store the results.

    Args:
        param_name (str): The name of the parameter being varied.
        vary_values (list): List of values for the varying parameter.
        simulation_params (dict): Base parameters for the simulation.

    Returns:
        tuple: Dictionaries of wait times and processing times, and a string of results.
    """
    wait_times = {}
    processing_times = {}
    results = ""

    for value in vary_values:
        params = simulation_params.copy()
        params[param_name] = value

        results += f"\nSimulation with {param_name} = {value}\n"
        results += f"Simulation starting: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"

        sim = JobMarketSim(**params)
        sim.run_simulation()

        results += f"Simulation ended: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        results += f"Total jobs arrived: {sim.jobs_arrived}\n"
        results += f"Total jobs processed: {sim.jobs_processed}\n"
        results += f"Jobs in queue: {len(sim.queue)}\n"

        avg_wait_time = sim.total_wait_time / sim.jobs_processed
        avg_processing_time = sim.total_processing_time / sim.jobs_processed

        results += f"Average wait time: {avg_wait_time:.2f}\n"
        results += f"Average processing time: {avg_processing_time:.2f}\n"

        wait_times[value] = avg_wait_time
        processing_times[value] = avg_processing_time

    return wait_times, processing_times, results


def create_and_save_plots(data_dict, plot_folder):
    """
    Create and save plots based on the simulation results.

    Args:
        data_dict (dict): Dictionary containing the simulation results.
        plot_folder (str): Folder to save the plots.

    Returns:
        str: The path of the saved plot file.
    """
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Performance Metrics", fontsize=16)

    create_subplot(
        axs[0, 0],
        data_dict["wait_n"],
        "Average Wait Time vs Number of Servers",
        "Number of Servers (n)",
        "Average Wait Time",
    )
    create_subplot(
        axs[0, 1],
        data_dict["processing_n"],
        "Average Processing Time vs Number of Servers",
        "Number of Servers (n)",
        "Average Processing Time",
    )
    create_subplot(
        axs[1, 0],
        data_dict["wait_arrival"],
        "Average Wait Time vs Arrival Rate",
        "Normalised Arrival Rate (nλ)",
        "Average Wait Time",
    )
    create_subplot(
        axs[1, 1],
        data_dict["processing_arrival"],
        "Average Processing Time vs Arrival Rate",
        "Normalised Arrival Rate (nλ)",
        "Average Processing Time",
    )

    plt.tight_layout()
    plot_filename = os.path.join(
        plot_folder, Util.generate_filename("performance_metrics", "png")
    )
    plt.savefig(plot_filename, dpi=300)
    plt.close()

    return plot_filename


def start_program():

    ensure_directory_exists(Config.RESULTS_FOLDER)
    ensure_directory_exists(Config.RESULTS_FOLDER)

    vary_n = [10, 100, 500, 1000, 1500, 2000, 2500, 3000]
    vary_beta = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    base_params = {"n": 1000, "beta": 0.3, "alpha": 0, "d_n": 10}

    wait_n, processing_n, results_n = run_simulation_and_store_results(
        "n", vary_n, base_params
    )
    wait_arrival, processing_arrival, results_beta = run_simulation_and_store_results(
        "beta", vary_beta, base_params
    )

    all_results = {
        "wait_n": wait_n,
        "processing_n": processing_n,
        "wait_arrival": wait_arrival,
        "processing_arrival": processing_arrival,
    }

    json_file_path = save_to_json(all_results, "simulation_results")
    txt_file_path = save_to_txt(results_n + results_beta, "simulation_details")
    plot_file_path = create_and_save_plots(all_results, Config.RESULTS_FOLDER)

    print(f"JSON results have been saved to {json_file_path}")
    print(f"Detailed results have been saved to {txt_file_path}")
    print(f"Plots have been generated and saved to {plot_file_path}")
