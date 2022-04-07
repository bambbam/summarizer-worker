from typing import List

from pydantic import BaseModel
from summarizer.domain.base import Repository
from summarizer.domain.model.feature import Feature

class FeatureData(BaseModel):
    key: str
    list_of_fature : List[Feature]



class FeatureRepository(Repository):
    def __init__(self, table):
        self.table = table

    def get(self, key):
        try:
            item = FeatureData(**(self.table.get_item(Key=key)['Item']))
            return [i for i in item.list_of_fature]
        except:
            return None
    
    def put(self, data:List[Feature], ttl=None):
        try:
            for item in data:
                self.table.put_item(Item=item)
        except:
            return
