from abc import ABC, abstractmethod

class CreateStrategy(ABC):
    @abstractmethod
    def create(self, object):
        pass