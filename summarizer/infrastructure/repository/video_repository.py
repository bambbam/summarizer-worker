from datetime import datetime
from time import time
from typing import Dict, Literal, Optional

from pydantic import BaseModel

from summarizer.domain.base import Repository
from summarizer.domain.model.video import Video
from summarizer.infrastructure.now import get_now
from summarizer.infrastructure.uuid import get_uuid


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
        try:
            item = VideoData(**(self.table.get_item(Key={"key": key})["Item"]))
            ret = Video(key=key, url=item.url, algorithm=self.algorithm)
        except:
            ret = None
        return ret

    def update_status(self, key: str, status: Literal['start', 'end']):
        try:
            item = VideoData(**(self.table.get_item(Key={"key": key})["Item"]))
            item.status = status
            self.table.put_item(Item=item.dict())
            return True
        except:
            return False
    def put(self, data: Video, ttl=None):
        now = get_now()
        try:
            item = VideoData(
                key=data.key,
                url=data.url,
                status="start",
                start_time=now,
                end_time=None,
            )
            self.table.put_item(Item=item.dict())
            return True
        except:
            return False
