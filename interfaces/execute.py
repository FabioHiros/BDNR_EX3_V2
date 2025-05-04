from abc import ABC, abstractmethod

class ExecuteStrategy(ABC):
    @abstractmethod
    def execute(self, db):
        pass