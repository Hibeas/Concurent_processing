import multiprocessing
import time
import os

def worker_process(pipe_in, pipe_out, worker_id):
    data = None
    print(f"Worker {worker_id} waiting for data...")
    
    while data is None:
        if pipe_in.poll(0.2):
            data = pipe_in.recv()
        else:
            pass 
    data.sort()
    pipe_out.send(data)



def main():
    start_time = time.perf_counter()

    file_name = "numbers.txt"
    
    if not os.path.exists(file_name):
        print(f"Error: {file_name} not found. Please create it first.")
        return
    

    with open(file_name, 'r') as f:
        content = f.read().replace(',', ' ')
        numbers = [int(x) for x in content.split()]
    
    if len(numbers) < 220:
        print(f"Warning: File only contains {len(numbers)} numbers. Proceeding anyway.")

    mid = len(numbers) // 2
    array1 = numbers[:mid]
    array2 = numbers[mid:]

    p1_to_w2_recv, p1_to_w2_send = multiprocessing.Pipe(duplex=False)
    p1_to_w3_recv, p1_to_w3_send = multiprocessing.Pipe(duplex=False)


    w2_to_p1_recv, w2_to_p1_send = multiprocessing.Pipe(duplex=False)
    w3_to_p1_recv, w3_to_p1_send = multiprocessing.Pipe(duplex=False)


    proc2 = multiprocessing.Process(target=worker_process, args=(p1_to_w2_recv, w2_to_p1_send, 2))
    proc3 = multiprocessing.Process(target=worker_process, args=(p1_to_w3_recv, w3_to_p1_send, 3))

    proc2.start()
    proc3.start()

    p1_to_w2_send.send(array1)
    p1_to_w3_send.send(array2)

    got_1 = False
    got_2 = False

    while not (got_1 and got_2):
        
        if not got_1:
            if w2_to_p1_recv.poll(0.2):
                sorted1 = w2_to_p1_recv.recv()
                got_1 = True
                print("Main received data from Worker 2")
            else:
                print("Main process waiting for Worker 2...")

        if not got_2:
            if w3_to_p1_recv.poll(0.2):
                sorted2 = w3_to_p1_recv.recv()
                got_2 = True
                print("Main received data from Worker 3")
            else:
                print("Main process waiting for Worker 3...")


    proc2.join()
    proc3.join()



    final_sorted = sorted(sorted1 + sorted2) #should be fast because it's timsort, beased on merge sort

    #final_sorted = sorted1 + sorted2#should be fast because it's timsort, beased on merge sort

    end_time = time.perf_counter()
    duration = end_time - start_time

    print(f"Successfully sorted {len(final_sorted)} numbers.")
    print(f"Execution Time: {duration:.6f} seconds")
    print(final_sorted)

if __name__ == "__main__":
    main()