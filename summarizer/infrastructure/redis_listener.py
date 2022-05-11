from summarizer.infrastructure.event_listener import EventListener


class RedisListener(EventListener):
    def __init__(self, key, redis):
        self.redis = redis
        self.key = key

    def size(self):
        return self.redis.llen(self.key)

    def get(self):
        return self.redis.rpop(self.key)
