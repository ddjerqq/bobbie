import time
import random


class Id(object):
    """
    the id of each object that we generate.
    this is a ripoff of discord's id system.
    """
    # 2004/02/16 10 am
    EPOCH = 107691120000
    __worker_increments = {i: 0 for i in range(32)}

    @classmethod
    def new(cls):
        # number of seconds since I was born lol
        id   = time.time_ns() // 10_000_000
        id  -= cls.EPOCH
        id <<= 5

        # internal worker id simulated
        worker_id = random.randrange(0, 32)  # 5 bits
        id  += worker_id
        id <<= 5

        # internal process id simulated
        id  += random.randrange(0, 32)       # 5 bits
        id <<= 12

        # for every ID that is generated on a process, this number is incremented
        id  += cls.__worker_increments[worker_id] % 4096
        cls.__worker_increments[worker_id] += 1

        return id
