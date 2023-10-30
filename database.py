import redis
class Database:
    def __init__(self, host, port):
        self.db = redis.Redis(host=host, port=port, decode_responses=True)
