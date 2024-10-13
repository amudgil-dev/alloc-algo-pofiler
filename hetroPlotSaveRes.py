from jump_model1 import JobMarketSim
import time
import collections
import json


def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


vary_n = [10, 100, 500, 1000, 1500, 2000, 2500, 3000]

wait_n = {}
processing_n = {}
final_yi = collections.defaultdict(list)

for n in vary_n:
    myparams = {"n": n, "beta": 0.3, "alpha": 0, "d_n": 10}

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

save_to_file(results, "mixed_erl_results.txt")

print("Results have been saved to mixed_erl_results.txt")
