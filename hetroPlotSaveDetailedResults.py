from jump_model1 import JobMarketSim
import time
import collections

vary_n = [10, 100, 500, 1000, 1500, 2000, 2500, 3000]

wait_n = {}
processing_n = {}
final_yi = collections.defaultdict(list)

# Open the file in append mode
with open("distributionResults.txt", "a") as f:
    f.write(f"\n--- New Simulation Run: {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n\n")

    for n in vary_n:
        myparams = {"n": n, "beta": 0.3, "alpha": 0, "d_n": 10}

        f.write(f"Simulation parameters: {myparams}\n")
        f.write(f"Simulation starting: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        sim = JobMarketSim(**myparams)
        yi_stats = sim.run_simulation()

        for k, v in yi_stats.items():
            final_yi[k].append(v)

        f.write(f"Simulation ended: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        f.write("yi_stats: " + str(yi_stats) + "\n")

        f.write(f"\nFinal stats:\n")
        f.write(f"Total jobs arrived: {sim.jobs_arrived}\n")
        f.write(f"Total jobs processed: {sim.jobs_processed}\n")
        f.write(f"Jobs in queue: {len(sim.queue)}\n")
        f.write(f"Average wait time: {sim.total_wait_time / sim.jobs_processed:.2f}\n")
        f.write(
            f"Average processing time: {sim.total_processing_time / sim.jobs_processed:.2f}\n"
        )

        wait_n[n] = sim.total_wait_time / sim.jobs_processed
        processing_n[n] = sim.total_processing_time / sim.jobs_processed

        f.write("\n")

    f.write("------------ yi vals --------------\n")

    for k, v in final_yi.items():
        average = [sum(x) / len(x) for x in zip(*v)]
        f.write(f"job class {k} yis: {average}\n")

    f.write("\nAverage Wait Time vs Number of Servers:\n")
    for n, wait_time in wait_n.items():
        f.write(f"n: {n}, Average Wait Time: {wait_time}\n")

    f.write("\nAverage Processing Time vs Number of Servers:\n")
    for n, proc_time in processing_n.items():
        f.write(f"n: {n}, Average Processing Time: {proc_time}\n")

print("All results have been saved to distributionResults.txt")
