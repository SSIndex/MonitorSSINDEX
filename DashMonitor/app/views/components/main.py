'''
Main Component Class Definition.
'''

# std imports
from typing import List

# 3rd party imports
from dash import html

# local imports
from DashMonitor.app.handlers.tab_utils import TabArgsProvider, main_tab_target_id
from DashMonitor.app.views.components.base_component import BaseComponent, DashComponent


class MainTabPanel(BaseComponent):
    '''
    Tab Body Component. Last wrapper around the different sections of the report.
    '''

    BODY_CLASS_NAME = 'tab-pane fade'
    ACTIVE_BODY_CLASS_NAME = 'tab-pane fade show active'

    def __init__(self, tab_name: str, view: DashComponent):
        self.tab_args_provider = TabArgsProvider()
        self.__dict__ = {**self.tab_args_provider(tab_name), **self.__dict__}
        self.view = view

    def render(self) -> html.Section:
        return html.Section(
            id=main_tab_target_id(self.id),
            className=(
                self.ACTIVE_BODY_CLASS_NAME if self.active else self.BODY_CLASS_NAME
            ),
            role='tabpannel',
            children=[self.view],
            **{'aria-labelledby': f'{self.id}-tab'},
        )


class Main(BaseComponent):
    '''
    Main Component. Main content will be declared here
    '''

    def __init__(self, tab_bodies: List[MainTabPanel]):
        self.tab_bodies = tab_bodies

    def render(self) -> html.Main:
        return html.Main(
            className='container container-fluid pt-2',
            children=[
                html.Section(
                    id='tabs-body',
                    className='tab-content',
                    children=[tab.render() for tab in self.tab_bodies],
                )
            ],
        )
