from pydantic import BaseModel
from abc import ABC, abstractmethod

class BaseVideo(BaseModel, ABC):
    @abstractmethod
    def read_video():
        ...

class BaseFeature(BaseModel, ABC):
    ...

class BaseVideoShortener(BaseModel, ABC):
    @staticmethod
    @abstractmethod
    def shorten(video: BaseVideo, feature: BaseFeature):
        ...

class BaseVideoFeatureExtractor(BaseModel, ABC):
    @staticmethod
    @abstractmethod
    def extract_feature(video: BaseVideo):
        ...
