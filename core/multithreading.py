import threading


def create_workers(number_of_threads, work, queue, *args):
    for _ in range(number_of_threads):
        t = threading.Thread(target=work, args=(queue, *args,))
        t.daemon = True
        t.start()
    return


def create_jobs(args, queue):
    if not args:
        from queue import Empty
        raise Empty()
    for arg in args:
        queue.put(arg)
    queue.join()
    return
