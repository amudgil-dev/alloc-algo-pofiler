"""
This module combines simulation and plotting functionality for a job market simulation.
It runs simulations with varying parameters, saves results, and generates plots.
"""

from app.models.jump_model import JobMarketSim
import time
import collections
import json
from config import Config
import os
from simdata.sim_parameters import RunParamA
from app.utils.util import Util, FileUtil, NumpyEncoder

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def start_program():

    vary_n = RunParamA.get_vary_n()  # pulling constatnt value
    wait_n = {}
    processing_n = {}
    final_yi = collections.defaultdict(list)

    for n in vary_n:

        myparams = RunParamA.get_params(n)

        print(f"sim starting: {time.time()}")
        sim = JobMarketSim(**myparams)

        yi_stats = sim.run_simulation()

        for k, v in yi_stats.items():
            final_yi[k].append(v)

        print(f"sim over: {time.time()}")

        print("yi_stats: ", yi_stats)

        print(f"\nFinal stats:")
        print(f"Total jobs arrived: {sim.jobs_arrived}")
        print(f"Total jobs processed: {sim.jobs_processed}")
        print(f"Jobs in queue: {len(sim.queue)}")
        print(f"Average wait time: {sim.total_wait_time / sim.jobs_processed:.2f}")
        print(
            f"Average processing time: {sim.total_processing_time / sim.jobs_processed:.2f}"
        )

        wait_n[n] = sim.total_wait_time / sim.jobs_processed
        processing_n[n] = sim.total_processing_time / sim.jobs_processed

    print("------------ yi vals --------------")

    for k, v in final_yi.items():
        average = [sum(x) / len(x) for x in zip(*v)]
        print(f"job class {k} yis: {average}")

    # Save results to file
    results = {
        "wait_n": wait_n,
        "processing_n": processing_n,
        "final_yi": {k: [list(v) for v in final_yi[k]] for k in final_yi},
    }

    print(f"---------- Saving the results to file ---------")
    prefix = "2class_exp_pstar_results"
    ext = "json"
    filename = Util.generate_filename(prefix, ext)
    file_path = os.path.join(Config.RESULTS_FOLDER, filename)
    FileUtil.save_as_json(results, file_path)

    print(f"Results have been saved to {file_path}.{ext}")
