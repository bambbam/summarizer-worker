from typing import Literal
from pydantic import BaseSettings

from summarizer.infrastructure.redis_listener import RedisListener

class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_key: str

    detector_model: Literal["yolov3", "tinyYolov3"]
    dynamodb_url: str
    class Config:
        env_file=".env"