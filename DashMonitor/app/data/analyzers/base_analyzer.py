'''
Base Analyzer
'''

# std imports
from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):

    def __init__(self, provider, app):
        self.__provider = provider
        self.__app = app

    @abstractmethod
    def _filter(self): ...

    @abstractmethod
    def _group(self): ...

    @abstractmethod
    def _aggregate(self): ...

    @abstractmethod
    def _having(self): ...

    @abstractmethod
    def _sort(self): ...

    @abstractmethod
    def execute(self):
        self._filter()
        self._group()
        self._aggregate()
        self._having()
        self._sort()
