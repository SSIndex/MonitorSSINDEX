'''
Base Components class for all components declared in this project.
'''

# std imports
from abc import ABC, abstractmethod

# 3rd party imports
from dash.development.base_component import Component as DashComponent


class BaseComponent(ABC):
    '''
    Base Component: exposes methods and properties all Components should implement.
    '''

    @abstractmethod
    def render(self) -> DashComponent:
        '''
        Render the Dash html components associated.
        '''
        ...
