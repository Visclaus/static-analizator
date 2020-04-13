# from q\ueue import Queue
import threading


def create_workers(NUMBER_OF_THREADS, work, queue, *args):
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work, args=(queue, *args,))
        t.daemon = True
        t.start()
    return


def create_jobs(ITEMS, queue):
    if not ITEMS:
        from queue import Empty
        raise Empty()
    for item in ITEMS:
        queue.put(item)
    queue.join()
    return
