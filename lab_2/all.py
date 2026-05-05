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

if __name__ == "__main__":
    N = 20000000
    M = 99
    num_procs = 4
    chunk = N // num_procs

    print("--- TASK 6")
    start_seq = time.time()
    seq_res = myFun_logic(0, N, M)
    duration_seq = time.time() - start_seq
    print(f"Result: {seq_res} | Time: {duration_seq:.4f}s\n")

    print("--- TASK 1, 2 & 4")
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
    print(f"Result: {total_par} | Time: {duration_par:.4f}s")

    print("--- TASK 3")
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
    print(f"Result with Lock: {shared_sum.value}\n")

    print("--- TASK 5")
    with multiprocessing.Pool(processes=num_procs) as pool:
        try:
            future_res = pool.apply_async(myFun_logic, (0, N, M))
            final_val = future_res.get(timeout=10) 
            print(f"Async Result Success: {final_val}")
        except multiprocessing.TimeoutError:
            print("The operation timed out!")