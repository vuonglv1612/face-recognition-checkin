from rq import Queue, Connection, Worker
from redis import Redis
from config import REDIS_URI, WORKER_QUEUE


def main():
    redis = Redis.from_url(REDIS_URI)
    with Connection(redis):
        worker = Worker([Queue(WORKER_QUEUE)])
        worker.work()


if __name__ == "__main__":
    main()
