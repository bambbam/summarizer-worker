from abc import ABC, abstractmethod
from typing import Any, List

from pydantic import BaseModel


class BaseFeature(BaseModel, ABC):
    ...


class BaseImage(ABC):
    @abstractmethod
    def extract(self, idx: int) -> List[BaseFeature]:
        ...


class BaseVideo(BaseModel, ABC):
    @abstractmethod
    def extract_feature(self) -> List[BaseFeature]:
        ...

    @abstractmethod
    def shorten(self, feature: BaseFeature):
        ...


class BaseDetector(BaseModel, ABC):
    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def extract(self, image: BaseImage, idx: int) -> List[BaseFeature]:
        ...

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class Repository(ABC):
    @abstractmethod
    def put(self, data, ttl=None):
        ...
    
    def get(self, entity_key):
        ...
