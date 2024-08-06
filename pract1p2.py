import multiprocessing

def producer(queue):
    items = range(10)
    for item in items:
        queue.put(item)

def consumer(queue):
    while True:
        item = queue.get()
        print(f"Consumed item: {item}")
        queue.task_done()

if __name__ == '__main__':
    queue = multiprocessing.Queue()

    producer_process = multiprocessing.Process(target=producer, args=(queue,))
    consumer_process = multiprocessing.Process(target=consumer, args=(queue,))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    queue.join()
    consumer_process.terminate()
