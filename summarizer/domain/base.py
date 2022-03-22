from pydantic import BaseModel
from typing import Any, List
from abc import ABC, abstractmethod

class BaseImage(BaseModel, ABC):
    class Config():
        arbitrary_types_allowed=True    
        
    @abstractmethod
    def extract():
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

class Singleton:
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    