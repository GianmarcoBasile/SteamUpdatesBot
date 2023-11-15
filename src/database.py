"""Module providing Database API."""

import redis
def initialize_db(host, port):
    """Initialize Database."""
    db = redis.Redis(host=host, port=port, decode_responses=True)
    return db
    