from model1 import JobMarketSim
from db_manager import db_dump, db_clear
import time


myparams = {"n": 100, "beta": 0.5, "alpha": 0.5, "d_n": 5, "max_jobs": 5000}

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


# db_clear()
db_dump(myparams, results)
print("added to db")
