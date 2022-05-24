from datetime import datetime
from time import time
from typing import Dict, Literal, Optional

from pydantic import BaseModel

from summarizer.domain.base import Repository
from summarizer.domain.model.video import Video
from summarizer.infrastructure.now import get_now


class VideoData(BaseModel):
    key: str
    user_name: str
    status: str
    start_time: str
    end_time: Optional[str]


class VideoDataRepository(Repository):
    def __init__(self, dynamodb, algorithm):
        self.table = dynamodb.Table("Video")
        self.algorithm = algorithm

    def get(self, key):
        try:
            item = VideoData(**(self.table.get_item(Key={"key": key})["Item"]))
        except:
            item = None
        return item

    def update_status(self, key: str, status: Literal['start', 'end']):
        try:
            item = VideoData(**(self.table.get_item(Key={"key": key})["Item"]))
            item.status = status
            self.table.put_item(Item=item.dict())
            return True
        except:
            return False
            
    def put(self, data: VideoData, ttl=None):
        now = get_now()
        try:
            data.status="end"
            data.end_time = now
            self.table.put_item(Item=data.dict())
            return True
        except:
            return False
