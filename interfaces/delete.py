from abc import ABC, abstractmethod

class DeleteStrategy(ABC):
    @abstractmethod
    def delete(self, db):
        pass