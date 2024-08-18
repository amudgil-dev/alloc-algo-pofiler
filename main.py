from jump_model1 import JobMarketSim
from db_manager import db_dump, db_clear
import time
from jump_model1_graphs import plot_jump_model1_results
from pprint import pprint

vary_n = [10, 100, 500, 1000, 1500, 2000]
vary_beta = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


myparams = {"n": 1000, "beta": 0.3, "alpha": 0, "d_n": 10, "max_jobs": 50000}

print(f"sim starting: {time.time()}")
sim = JobMarketSim(**myparams)


results = sim.run_simulation()
print(f"sim over: {time.time()}")
print(f"\nFinal stats:")
print(f"Total jobs arrived: {sim.jobs_arrived}")
print(f"Total jobs processed: {sim.jobs_processed}")
print(f"Jobs in queue: {len(sim.queue)}")
print(f"Average wait time: {sim.total_wait_time / sim.jobs_processed:.2f}")
print(f"Average processing time: {sim.total_processing_time / sim.jobs_processed:.2f}")

print("---------")
pprint(len(results))


# plotting results
plot_jump_model1_results(results, sim)

db_clear()
db_dump(myparams, results)
print("added to db")
