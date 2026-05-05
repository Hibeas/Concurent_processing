import multiprocessing
import time
import sys

def myFun(start, end, m):
    return sum([x * (x - m) for x in range(start, end)])

def worker_task(start, end, m, conn, cond, shared_count):
    try:
        result = myFun(start, end, m)
        
        conn.send(result)
        conn.close() 

        with cond:
            shared_count.value += 1
            cond.notify_all() 
            
    except Exception as e:
        print(f"Worker Error at range {start}-{end}: {e}")

def run_multiprocessing_v4(total_n, m, num_procs=4):
    manager = multiprocessing.Manager()
    cond = manager.Condition()
    shared_count = manager.Value('i', 0)
    
    pipes = [multiprocessing.Pipe(duplex=False) for _ in range(num_procs)]
    processes = []
    chunk_size = total_n // num_procs
    
    start_time = time.time()

    for i in range(num_procs):
        start_range = i * chunk_size
        end_range = total_n if i == num_procs - 1 else (i + 1) * chunk_size
        
        p = multiprocessing.Process(
            target=worker_task, 
            args=(start_range, end_range, m, pipes[i][1], cond, shared_count)
        )
        processes.append(p)
        p.start()

    total_sum = 0
    with cond:
        while shared_count.value < num_procs:
            if not cond.wait(timeout=5.0): 
                print("Main process timed out waiting for workers.")
                break

    for i in range(num_procs):
        try:
            if pipes[i][0].poll(1.0): 
                total_sum += pipes[i][0].recv()
        except Exception as e:
            print(f"Pipe receive error: {e}")

    for p in processes:
        p.join()
        
    return time.time() - start_time, total_sum



def run_sequential(n, m):
    start_time = time.time()
    result = sum([x * (x - m) for x in range(n)])
    return time.time() - start_time, result



#previous code for multiprocessing_lab3.py
def worker_queue(start, end, m, queue):
    result = myFun(start, end, m)
    queue.put(result)

def worker_lock(start, end, m, shared_val, lock):
    result = myFun(start, end, m)
    with lock:
        shared_val.value += result
    
def myFun_logic(start, end, m, shared_sum, semaphore):
    try:
        local_result = sum([x * (x - m) for x in range(start, end)])
        if semaphore.acquire(timeout=5.0):
            try:
                shared_sum.value += local_result
            finally:
                semaphore.release()
        else:
            print(f"Process for range {start}-{end} timed out.")
            
    except Exception as e:
        print(f"Error in process: {e}")

def run_parallel(total_n, m, num_procs=4):
    #shared_sum = multiprocessing.Value('d', 0.0) 
    manager=multiprocessing.Manager()
    shared_sum=manager.Value("i",0)

    sem = multiprocessing.Semaphore(1)
    
    chunk_size = total_n // num_procs
    processes = []
    
    start_time = time.time()
    for i in range(num_procs):
        start_range = i * chunk_size
        end_range = total_n if i == num_procs - 1 else (i + 1) * chunk_size
        
        p = multiprocessing.Process(target=myFun_logic, args=(start_range, end_range, m, shared_sum, sem))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
        
    return time.time() - start_time, shared_sum.value

def run_sequential(n, m):
    start_time = time.time()
    result = sum([x * (x - m) for x in range(n)])
    return time.time() - start_time, result



if __name__ == "__main__":
    N = 20_000_000
    M = 99
    ITERATIONS = 50 
    num_procs = 4
    chunk = N // num_procs
    
    
    seq_time, seq_res = run_sequential(N, M)
    print(f"\nSequential Time: {seq_time:.4f}s | Result: {seq_res}\n\n")

    parallel_times = []
    final_parallel_res = 0
    print(f"--- Running Lab 4: Pipes and Condition Variables ---")
    print(f"Executing {ITERATIONS} parallel runs...")
    for i in range(ITERATIONS):
        p_time, p_res = run_multiprocessing_v4(N, M)
        parallel_times.append(p_time)
        final_parallel_res = p_res
            
    mean_t = sum(parallel_times) / ITERATIONS
    delta_t = (max(parallel_times) - min(parallel_times)) / 2
    
    print("\n" + "-"*30)
    print(f"Validation: {'SUCCESS' if seq_res == final_parallel_res else 'FAILURE'}")
    print(f"Parallel Mean Time: {mean_t:.4f}s")
    print(f"Uncertainty (Delta T): {delta_t:.4f}s")
    print("-"*30)
    
    
    #previous code for multiprocessing_lab3.py
    print("\n" + "-"*30)
    print(f"\nRunning Parallel Version (lab 3) {ITERATIONS} times...")
    parallel_times = []
    final_val = 0
    
    for i in range(ITERATIONS):
        p_time, p_res = run_parallel(N, M)
        parallel_times.append(p_time)
        final_val = p_res 
    final_val_int = int(final_val)
    print("\n" + "-"*30)
    print(f"\nVerification: {'SUCCESS' if seq_res == final_val_int else 'FAILURE'}")

    mean_t = sum(parallel_times) / ITERATIONS
    delta_t = (max(parallel_times) - min(parallel_times)) / 2
    
    print(f"Parallel Mean Time: {mean_t:.4f}s")
    print(f"Uncertainty : {delta_t:.4f}s")
    print("-" * 30)

    print("\n" + "-"*30)
    print("Running lab 2")
    print("--- TASK 6")
    duration_seq=[]
    for i in range(ITERATIONS):
        start_seq = time.time()
        seq_res = myFun(0, N, M)
        duration_seq.append(time.time() - start_seq)

    mean_t = sum(duration_seq) / ITERATIONS
    delta_t = (max(duration_seq) - min(duration_seq)) / 2
    
    
    print("\n" + "-"*30)
    print(f"Parallel Mean Time: {mean_t:.4f}s")
    print(f"Uncertainty : {delta_t:.4f}s")
    print("\n" + "-"*30)


