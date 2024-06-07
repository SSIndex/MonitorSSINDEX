'''
Header Class Definition.
'''

# std imports
from typing import List

# 3rd party imports
from dash import html


class HeaderTabBtn:
    '''
    Header Tab. Each Tab Button associated to a Tab Content for the Main element.
    '''

    def __init__(self, tab_id: str, title: str, active: bool):
        self.id = tab_id
        self.target = f'#{tab_id}'
        self.title = title
        self.active = active

    def render(self):
        '''
        Generate de Dash Component for the HeaderTabButton
        '''
        btn_class_names = 'nav-link text-light'
        btn_class_names += ' active' if self.active else ''

        aria_selected = 'true' if self.active else 'false'

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


class Header:
    '''
    Header Element for API. it includes the navbar and the Tab options.
    '''

    def __init__(self, logo_source: str, logo_name: str, tabs: List[HeaderTabBtn]):
        self.logo_source = logo_source
        self.logo_name = logo_name
        self.tab_list = tabs

    def render(self):
        '''
        Generate de Dash Component for the Header
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
                                        html.Div(
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
                                                                            style={
                                                                                'height': '2.5rem'
                                                                            },
                                                                        )
                                                                    ]
                                                                ),
                                                                html.Figcaption(
                                                                    children=[
                                                                        self.logo_name
                                                                    ],
                                                                    style={
                                                                        'font-size': '.6rem'
                                                                    },
                                                                ),
                                                            ]
                                                        )
                                                    ],
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className='col-10',
                                            children=[
                                                html.Div(
                                                    className='container',
                                                    children=[
                                                        html.Ul(
                                                            className='nav nav-underline nav-fill justify-content-center fs-4',
                                                            id='TabButtonsList',
                                                            role='tablist',
                                                            children=list(
                                                                map(
                                                                    lambda x: x.render(),
                                                                    self.tab_list,
                                                                )
                                                            ),
                                                        )
                                                    ],
                                                )
                                            ],
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ],
        )
