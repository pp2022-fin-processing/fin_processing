from abc import ABC, abstractmethod

class APIProvider(ABC):
    @abstractmethod
    def stock(self):
        pass

    @abstractmethod
    def forex(self):
        pass

    @abstractmethod
    def indices(self):
        pass
