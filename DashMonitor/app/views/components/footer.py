'''
Footer Class Definition.
'''

# std imports

# 3rd party imports
from dash import html

# local imports
from DashMonitor.app.views.components.base_component import BaseComponent


class Footer(BaseComponent):

    def __init__(self): ...

    def render(self) -> html.Footer:
        return html.Footer(
            className='footer p-5 text-center',
            children=[
                html.Div(
                    className='container',
                    children=[
                        html.P(
                            className='mb-0 text-ssindex-footer-text',
                            children=['© 2024 SSINDEX'],
                        )
                    ],
                )
            ],
        )
