'''
Tab Utils Classes.
'''

# std imports
from typing import Dict, Optional, Set, Union


def main_tab_target_id(element_id: str) -> str:
    return f'main-tab-{element_id}'


class TabArgsProvider:
    '''
    Class for validating and storing correct tab names across components.
    It uses the singleton pattern to avoid recomputing the tabs queries for
    each component associated with this class.
    '''

    _instance: Optional['TabArgsProvider'] = None
    _tabs_args: Dict[str, Dict[str, Union[str, bool]]] = {
        'GENERAL': {'id': 'general-analysis', 'active': True},
        'SASB': {'id': 'sasb-analysis', 'active': False},
        'SSINDEX': {'id': 'ssindex-analysis', 'active': False},
        'MAP': {'id': 'geographic-analysis', 'active': False},
        'TIME TREND': {'id': 'benchmark-analysis', 'active': False},
    }
    _tabs_available: Set[str] = set()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TabArgsProvider, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize_tabs()
        return cls._instance

    def _initialize_tabs(self) -> None:
        '''Initialize the available tabs.'''
        self._tabs_available = set(self._tabs_args.keys())

    def validate(self, tab_name: str) -> None:
        '''
        Checks if tab_name is in the available tabs dict.

        Args:
            tab_name (str): The name of the tab to validate.

        Raises:
            KeyError: If the tab_name is not valid.
        '''
        if tab_name not in self._tabs_available:
            raise KeyError(
                f'Invalid tab_name: {tab_name}. Available tabs: {self._tabs_available}'
            )

    def __call__(self, tab_name: str) -> Dict[str, Union[str, bool]]:
        '''
        Returns the arguments for the specified tab.

        Args:
            tab_name (str): The name of the tab to retrieve arguments for.

        Returns:
            Dict[str, Any]: The arguments for the tab.
        '''
        self.validate(tab_name)
        return self._tabs_args[tab_name]
