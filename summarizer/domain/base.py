from abc import ABC, abstractmethod
from typing import Any, List

from pydantic import BaseModel


class BaseFeature(BaseModel, ABC):
    ...


class BaseImage(ABC):
    ...


class BaseVideo(BaseModel, ABC):
    @abstractmethod
    def shorten(self, feature: BaseFeature):
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
