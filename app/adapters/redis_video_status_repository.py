import redis
import os

class RedisVideoStatusRepository:
    def __init__(self):
        self.redis_host = os.environ.get('REDIS_HOST')
        self.redis_port = int(os.environ.get('REDIS_PORT', 6379))
        self.redis_password = os.environ.get('REDIS_PASSWORD', None)

        self.client = redis.Redis(
            host=self.redis_host, 
            port=self.redis_port, 
            password=self.redis_password, 
            decode_responses=True
        )

    def get_user_video_keys(self, user_email: str):
        keys_pattern = f"video-status:{user_email}:*"
        return self.client.keys(keys_pattern)

    def get_video_status_data(self, key: str):
        return self.client.hgetall(key)
