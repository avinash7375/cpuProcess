import multiprocessing
import time

def producer(shm, buffer_size, empty, full):
    items = range(10)
    index = 0
    while True:
        if empty.acquire():
            shm.buf[index % buffer_size] = items[index]
            index += 1
            full.release()
            empty.release()
            time.sleep(1)

def consumer(shm, buffer_size, empty, full):
    index = 0
    while True:
        if full.acquire():
            item = shm.buf[index % buffer_size]
            print(f"Consumed item: {item}")
            index += 1
            empty.release()
            full.release()
            time.sleep(1)

if __name__ == '__main__':
    buffer_size = 5
    shm = multiprocessing.shared_memory.SharedMemory(create=True, size=buffer_size * 4)
    empty = multiprocessing.Semaphore(buffer_size)
    full = multiprocessing.Semaphore(0)

    producer_process = multiprocessing.Process(target=producer, args=(shm, buffer_size, empty, full))
    consumer_process = multiprocessing.Process(target=consumer, args=(shm, buffer_size, empty, full))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()

    shm.close()
    shm.unlink()
