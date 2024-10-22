from abc import ABC, abstractmethod
from typing import AnyStr


class HtmlBasic(ABC):

    @classmethod
    @abstractmethod
    def html_connect(cls, html: AnyStr):
        raise NotImplemented
