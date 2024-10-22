from abc import ABC, abstractmethod


class BasicBrowser(ABC):

    @classmethod
    @abstractmethod
    def browser_connect(cls):
        raise NotImplemented
