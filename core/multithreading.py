# from q\ueue import Queue
import threading


def create_workers(NUMBER_OF_THREADS, work, queue, code_list):
    for index in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work, args=(queue, code_list[index]))
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
