'''
Base Provider class for all data providers declared in this project.
'''

# std imports
from abc import ABC, abstractmethod

# 3rd party imports


class SingletonProvider:
    '''
    Providers should be singletons, not be created many times on runtime.
    '''

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonProvider, cls).__new__(cls)
        return cls._instance


class BaseProvider(SingletonProvider, ABC):
    '''
    BaseProvider for all data providers available in the app
    '''

    @abstractmethod
    def __call__(self):
        '''
        Method to call provider for presenting access to data
        '''
        ...
