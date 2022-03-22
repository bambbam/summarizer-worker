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
