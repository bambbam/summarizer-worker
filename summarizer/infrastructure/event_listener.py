from abc import ABC, abstractmethod

class EventListener(ABC):
    @abstractmethod
    def get(self):
        ...

    @abstractmethod
    def size(self):
        ...

    def isEmpty(self):
        return self.size() == 0
