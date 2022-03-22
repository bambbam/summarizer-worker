from abc import ABC, abstractmethod
from typing import Any, List

from pydantic import BaseModel


class BaseImage(ABC):
    @abstractmethod
    def extract(idx: int):
        ...


class BaseFeature(BaseModel, ABC):
    ...


class BaseVideo(BaseModel, ABC):
    @abstractmethod
    def extract_feature() -> List[BaseFeature]:
        ...

    @abstractmethod
    def shorten(feature: BaseFeature):
        ...


class BaseDetector(BaseModel, ABC):
    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def extract(self, image: BaseImage, idx: int):
        ...


class Singleton:
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
