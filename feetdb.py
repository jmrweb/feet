import subprocess
import time

import redis



class Singleton(type):
    """ A metaclass for singleton purpose. Every singleton class should inherit from this class by 'metaclass=Singleton'. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FeetDB(metaclass=Singleton):
    """Singleton class for redis database"""

    def __init__(self):
        self.db = subprocess.Popen("redis-server")
        time.sleep(1)
        self.dbindex = 0
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=self.dbindex)
        self.r.config_set('notify-keyspace-events', 'KEA')
        self.connected = True
        

    @property
    def conn(self) -> redis.Redis:
        """Return redis connection"""
        return self.r
    

    def close(self) -> None:
        """Soft shutdown of redis server"""
        self.connected = False
        self.r.flushdb()
        self.r.shutdown()
        # self.db.kill()red