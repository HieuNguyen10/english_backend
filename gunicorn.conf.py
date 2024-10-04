from multiprocessing import cpu_count


def max_workers():
    return cpu_count()


bind = '127.0.0.1:5000'
backlog = 2048

threads = 3  # each worker has 3 threads
# workers = int((2 * max_workers() + 1) / threads)
workers = 5
worker_class = 'uvicorn.workers.UvicornWorker'
# worker_connections = 1000
timeout = 600
keepalive = 10
errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
