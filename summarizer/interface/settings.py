from pydantic import BaseSettings
from pydantic import BaseSettings

from summarizer.infrastructure.redis_listener import RedisListener

class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_key: str

    detector_model: str

    class Config:
        env_file=".env"