import json
from decimal import Decimal
from typing import List

from pydantic import BaseModel

from summarizer.domain.base import Repository
from summarizer.domain.model.feature import VideoFeature
from summarizer.exception import DatabaseException


class FeatureData(VideoFeature):
    ...


class FeatureRepository(Repository):
    def __init__(self, dynamodb):
        self.table = dynamodb.Table("Feature")

    def get(self, key):
        try:
            return VideoFeature(**(self.table.get_item(Key={"key": key})["Item"]))
        except:
            raise DatabaseException(f"{self.__class__} get method fail")        

    def put(self, data: VideoFeature, ttl=None):
        try:
            item = json.loads(json.dumps(data.dict()), parse_float=Decimal)
            self.table.put_item(Item=item)    
        except:
            raise DatabaseException(f"{self.__class__} put method fail")


class ShortedVideoRepository(Repository):
    def __init__(self, dynamodb):
        self.table = dynamodb.Table("ShortedVideo")
    
    def get(self,key):
        ...