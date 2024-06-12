'''
Header Class Definition.
'''

# std imports
from typing import List

# 3rd party imports
from dash import html

# local imports
from DashMonitor.app.handlers.tab_utils import TabArgsProvider
from DashMonitor.app.views.components.base_component import BaseComponent


class HeaderTabBtn(BaseComponent):
    '''
    Header Tab. Each Tab Button associated to a Tab Content for the Main element.
    '''

    BASE_BUTTON_CLASS_NAME = 'nav-link text-light'
    ACTIVE_BUTTON_CLASS_NAME = 'nav-link text-light active'

    def __init__(self, tab_name: str):
        self.tab_args_provider = TabArgsProvider()
        self.__dict__ = {**self.tab_args_provider(tab_name), **self.__dict__}
        self.title = tab_name
        self.target = f'#{self.id}'

    def render(self):
        '''
        Generate de Dash Component for the HeaderTabButton
        '''
        aria_selected = 'false'
        btn_class_names = self.BASE_BUTTON_CLASS_NAME
        if self.active:
            aria_selected = 'true'
            btn_class_names = self.ACTIVE_BUTTON_CLASS_NAME

        return html.Li(
            className='nav-item',
            role='presentation',
            disable_n_clicks=True,
            children=[
                html.Button(
                    className=btn_class_names,
                    id=self.id,
                    type='button',
                    role='tab',
                    children=[self.title],
                    style={'font-weight': 'normal'},
                    **{
                        'data-bs-toggle': 'tab',
                        'data-bs-target': self.target,
                        'aria-controls': self.id,
                        'aria-selected': aria_selected,
                    },
                )
            ],
        )


class Header(BaseComponent):
    '''
    Header Element for API. it includes the navbar and the Tab options.
    '''

    def __init__(self, logo_source: str, logo_name: str, tabs: List[HeaderTabBtn]):
        self.logo_source = logo_source
        self.logo_name = logo_name
        self.tab_list = tabs

    def render_logo(self) -> html.Div:
        '''
        Generate the Dash Partial Component for the logo
        '''
        return html.Div(
            className='col-2',
            children=[
                html.A(
                    href='/',
                    className='navbar-brand text-light',
                    children=[
                        html.Figure(
                            children=[
                                html.Picture(
                                    children=[
                                        html.Img(
                                            alt=self.logo_name,
                                            src=self.logo_source,
                                            style={'height': '2.5rem'},
                                        )
                                    ]
                                ),
                                html.Figcaption(
                                    children=[self.logo_name],
                                    style={'font-size': '.6rem'},
                                ),
                            ]
                        )
                    ],
                )
            ],
        )

    def render_tabs(self) -> html.Div:
        '''
        Generate the Dash Partial Component for the tabs.
        '''
        return html.Div(
            className='col-10',
            children=[
                html.Div(
                    className='container',
                    children=[
                        html.Ul(
                            className='nav nav-underline nav-fill justify-content-center fs-4',
                            id='TabButtonsList',
                            role='tablist',
                            children=[tab.render() for tab in self.tab_list],
                        )
                    ],
                )
            ],
        )

    def render(self) -> html.Header:
        '''
        Generate the Dash Component for the Header
        '''
        return html.Header(
            className='bg-dark text-white',
            children=[
                html.Nav(
                    className='navbar navbar-expand-lg',
                    children=[
                        html.Div(
                            className='container pb-0',
                            children=[
                                html.Div(
                                    className='row w-100',
                                    children=[
                                        self.render_logo(),
                                        self.render_tabs(),
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ],
        )
