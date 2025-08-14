import time
import multiprocessing
import threading

def cpu_worker(target_load, duration):
    """Keeps CPU at target load percentage for duration."""
    if not (0 <= target_load <= 100):
        raise ValueError("target_load must be between 0 and 100")
    
    period = 0.1  # seconds for each control cycle
    busy_time = period * (target_load / 100)
    idle_time = period - busy_time

    end_time = time.time() + duration
    while time.time() < end_time:
        start = time.time()
        while (time.time() - start) < busy_time:
            pass  # Burn CPU
        time.sleep(idle_time)

def simulate_cpu_spike(duration=30, cpu_percent=85):
    """Run on all CPU cores."""
    num_cores = multiprocessing.cpu_count()
    print(f"Simulating {cpu_percent}% CPU usage on {num_cores} cores for {duration}s...")
    threads = []
    for _ in range(num_cores):
        t = threading.Thread(target=cpu_worker, args=(cpu_percent, duration))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("CPU spike simulation completed.")

if __name__ == '__main__':
    # Spike CPU to 85% for 30 seconds
    simulate_cpu_spike(duration=30, cpu_percent=85)
