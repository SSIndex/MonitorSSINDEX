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
  def execute(self):
    ...

