from abc import ABC, abstractmethod

class ReadStrategy(ABC):
    @abstractmethod
    def read(self, db):
        pass