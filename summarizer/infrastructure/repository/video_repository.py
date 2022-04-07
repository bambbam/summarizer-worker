from datetime import datetime
from time import time
from typing import Dict, Optional
from pydantic import BaseModel
from summarizer.domain.base import Repository
from summarizer.domain.model.video import Video

class VideoData(BaseModel):
    key: str
    url: str
    status: str
    start_time: str
    end_time: Optional[str]


class VideoRepository(Repository):
    def __init__(self, table, algorithm):
        self.table = table
        self.algorithm=algorithm

    def get(self, key):
        item = VideoData(**(self.table.get_item(Key={"key":key})['Item']))
        return Video(url=item.url, algorithm=self.algorithm)
        
    def put(self, data:Video, ttl=None):
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        item = VideoData(
            key=f'{now}', #TODO change key value
            url=data.url,
            status="start2",
            start_time=now,
            end_tmie=None
        )
        self.table.put_item(Item=item.dict())