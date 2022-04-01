from dependency_injector import containers, providers
from redis import Redis

from summarizer.infrastructure.redis_listener import RedisListener

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    redis = providers.Singleton(Redis, host=config.redis_host, port=config.redis_port)

    redis_listener = providers.Factory(RedisListener, redis=redis, key=config.redis_key)
    