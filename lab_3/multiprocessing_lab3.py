import multiprocessing
import time

def myFun_logic(start, end, m):
    return sum([x * (x - m) for x in range(start, end)])

def worker_queue(start, end, m, queue):
    result = myFun_logic(start, end, m)
    queue.put(result)

def worker_lock(start, end, m, shared_val, lock):
    result = myFun_logic(start, end, m)
    with lock:
        shared_val.value += result
    
def myFun(start, end, m, shared_sum, semaphore):
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
        
        p = multiprocessing.Process(target=myFun, args=(start_range, end_range, m, shared_sum, sem))
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
    ITERATIONS = 20
    num_procs = 4
    chunk = N // num_procs
    
    print(f"Starting Sequential Version...")
    seq_time, seq_res = run_sequential(N, M)
    print(f"Sequential Time: {seq_time:.4f}s | Result: {seq_res}")
    
    print(f"\nRunning Parallel Version {ITERATIONS} times...")
    parallel_times = []
    final_val = 0
    
    for i in range(ITERATIONS):
        p_time, p_res = run_parallel(N, M)
        parallel_times.append(p_time)
        final_val = p_res 
        if i % 5 == 0: print(f"Iteration {i} complete...")
    final_val_int = int(final_val)
    
    print(f"Sequential Time: {seq_time:.4f}s | Result: {seq_res} | {final_val_int}")
    print(f"\nVerification: {'SUCCESS' if seq_res == final_val_int else 'FAILURE'}")

    mean_t = sum(parallel_times) / ITERATIONS
    delta_t = (max(parallel_times) - min(parallel_times)) / 2
    
    print("-" * 30)
    print(f"Parallel Mean Time: {mean_t:.4f}s")
    print(f"Uncertainty : {delta_t:.4f}s")
    print("-" * 30)


    print("Info from lab 2")
    print("--- TASK 6")
    duration_seq=[]
    for i in range(ITERATIONS):
        start_seq = time.time()
        seq_res = myFun_logic(0, N, M)
        duration_seq.append(time.time() - start_seq)

    mean_t = sum(duration_seq) / ITERATIONS
    delta_t = (max(duration_seq) - min(duration_seq)) / 2
    print(f"Parallel Mean Time: {mean_t:.4f}s")
    print(f"Uncertainty : {delta_t:.4f}s")

    #print("--- TASK 1, 2 & 4")
    result_queue = multiprocessing.Queue()
    processes = []
    start_par = time.time()

    for i in range(num_procs):
        s_range, e_range = i * chunk, (i + 1) * chunk
        p = multiprocessing.Process(target=worker_queue, args=(s_range, e_range, M, result_queue))
        processes.append(p)
        p.start()

    partial_results = [result_queue.get() for _ in range(num_procs)]
    
    for p in processes:
        p.join() 
    
    total_par = sum(partial_results)
    duration_par = time.time() - start_par
    #print(f"Result: {total_par} | Time: {duration_par:.4f}s")

   # print("--- TASK 3")
    mutex = multiprocessing.Lock()
    shared_sum = multiprocessing.Value('d', 0.0)
    lock_procs = []

    for i in range(num_procs):
        s_range, e_range = i * chunk, (i + 1) * chunk
        p = multiprocessing.Process(target=worker_lock, args=(s_range, e_range, M, shared_sum, mutex))
        lock_procs.append(p)
        p.start()

    for p in lock_procs:
        p.join()
    #print(f"Result with Lock: {shared_sum.value}\n")
