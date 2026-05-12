import multiprocessing
import time
import os

def bubble_sort(mylist):
    n = len(mylist)
    for i in range(n-1):
        for j in range(n-i-1):
            if mylist[j] > mylist[j+1]:
                mylist[j], mylist[j+1] = mylist[j+1], mylist[j]
    return mylist

def worker_process(input_queue, output_queue, worker_id):
    try:
        print(f"Worker {worker_id} waiting for data...")
        data = input_queue.get(timeout=4)
        sorted_data = bubble_sort(data)
        output_queue.put(sorted_data)
    except Exception as e:
        print(f"Worker {worker_id} error or timeout: {e}")

def main():
    start_time = time.perf_counter()

    file_name = "numbers.txt" 
    if not os.path.exists(file_name):
        print(f"Error: {file_name} not found.")
        return

    with open(file_name, 'r') as f:
        content = f.read().replace(',', ' ')
        numbers = [int(x) for x in content.split()]

    print(f"Not sorted array : {numbers}")
    mid = len(numbers) // 2
    array1 = numbers[:mid]
    array2 = numbers[mid:]
 
    q_in = multiprocessing.Queue()
    results_q = multiprocessing.Queue()

    proc2 = multiprocessing.Process(target=worker_process, args=(q_in, results_q, 2))
    proc3 = multiprocessing.Process(target=worker_process, args=(q_in, results_q, 3))

    proc2.start()
    proc3.start()

    q_in.put(array1)
    q_in.put(array2)

    final = []
    while len(final) < 2:
        result = results_q.get(timeout = 4) 
        final.append(result)
        print(f"Main received part {len(final)}/2")

    proc2.join()
    proc3.join()

    final_sorted = sorted(final[0] + final[1])
    
    duration = time.perf_counter() - start_time
    print(f"Successfully sorted array : {final_sorted}")
    print(f"Execution Time: {duration:.6f} seconds")

if __name__ == "__main__":
    main()