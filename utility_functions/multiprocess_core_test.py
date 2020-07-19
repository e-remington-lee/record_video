import multiprocessing
from multiprocessing import Process
import time

def worker(count):
    time.sleep(5)
    print(f"worker {count} done")

processes = []

def main():
    for x in range(1,50):
        p = Process(target=worker, args=(x,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == "__main__":
    print(multiprocessing.cpu_count())
    # We have 12 cores, 24 logic cores. So since the process does not utilize the CPU's 100%, 
    # we can feel safe having more AI processes than cores for someones CPU. So we can have valence detection, face, sound, and a fusion algorithm.
    main()