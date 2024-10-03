'''
Table Footer Definition
'''

from typing import Optional
from DashMonitor.app.views.components.base_component import BaseComponent

from dash import html


class TableFooter(BaseComponent):
    '''
    Table Footer component. Generates a tfoot for a table.
    '''

    def __init__(self, footer_data):
        self.footer_data = footer_data

    def render(self) -> Optional[html.Tfoot]:
        """
        Renders the table footer if footer_data is present.
        """
        return (
            html.Tfoot(
                className='border-top text-center',
                children=[
                    html.Tr(
                        children=[
                            (
                                html.Th(val)
                                if i == 0
                                else html.Td(val, className='text-center')
                            )
                            for i, val in enumerate(self.footer_data)
                        ]
                    )
                ],
            )
            if self.footer_data
            else None
        )
