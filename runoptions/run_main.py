from app.models.jump_model import JobMarketSim
from app.db.db_manager import db_dump, db_clear
import time
from app.models.jump_model_graphs import plot_jump_model1_results
from pprint import pprint
from simdata.sim_parameters import RunParamA

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def start_program():
    n = 1000
    myparams = RunParamA.get_params(n)

    print(f"sim starting: {time.time()}")
    sim = JobMarketSim(**myparams)

    results = sim.run_simulation()
    print(f"sim over: {time.time()}")
    print(f"\nFinal stats:")
    print(f"Total jobs arrived: {sim.jobs_arrived}")
    print(f"Total jobs processed: {sim.jobs_processed}")
    print(f"Jobs in queue: {len(sim.queue)}")
    print(f"Average wait time: {sim.total_wait_time / sim.jobs_processed:.2f}")
    print(
        f"Average processing time: {sim.total_processing_time / sim.jobs_processed:.2f}"
    )

    print("---------")
    pprint(len(results))
