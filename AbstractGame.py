from abc import ABCMeta, abstractmethod

class AbstractGame:
    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def startGame(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def terminate(self, **kwargs):
        raise NotImplementedError