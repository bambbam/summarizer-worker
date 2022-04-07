import json
from typing import List
from decimal import Decimal


from pydantic import BaseModel
from summarizer.domain.base import Repository
from summarizer.domain.model.feature import VideoFeature

class FeatureData(VideoFeature):
    ...



class FeatureRepository(Repository):
    def __init__(self, table):
        self.table = table

    def get(self, key):
        try:
            return FeatureData(**(self.table.get_item(Key={"key":key})['Item']))
        except:
            return None
    
    def put(self, data:VideoFeature, ttl=None):
        try:
            item = json.loads(json.dumps(data.dict()), parse_float=Decimal)
            self.table.put_item(Item=item)
        except:
            return