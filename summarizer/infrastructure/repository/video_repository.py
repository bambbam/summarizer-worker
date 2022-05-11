from datetime import datetime
from time import time
from typing import Dict, Optional

from pydantic import BaseModel

from summarizer.domain.base import Repository
from summarizer.domain.model.video import Video
from summarizer.infrastructure.now import get_now


class VideoData(BaseModel):
    key: str
    url: str
    status: str
    start_time: str
    end_time: Optional[str]


class VideoRepository(Repository):
    def __init__(self, dynamodb, algorithm):
        self.table = dynamodb.Table("Video")
        self.algorithm = algorithm

    def get(self, key):
        item = VideoData(**(self.table.get_item(Key={"key": key})["Item"]))
        return Video(key=key, url=item.url, algorithm=self.algorithm)

    def put(self, data: Video, ttl=None):
        now = get_now()
        item = VideoData(
            key=f"{now}",  # TODO change key value
            url=data.url,
            status="start",
            start_time=now,
            end_time=None,
        )
        print(item)
        self.table.put_item(Item=item.dict())
