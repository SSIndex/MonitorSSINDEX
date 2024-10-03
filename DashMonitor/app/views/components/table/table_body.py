'''
Table Body Definition
'''

from typing import List, Optional
from DashMonitor.app.views.components.base_component import BaseComponent
from dash import html


class TableBody(BaseComponent):
    '''
    Table Body component. Generates a tbody for a table.
    '''

    def __init__(self, rows: List[html.Tr] | html.Tr, class_name: Optional[str] = ''):
        self.rows = rows
        self.class_name = class_name

    def render(self) -> html.Tbody:
        """
        Renders the table body.
        """
        return html.Tbody(
            className=self.class_name,
            children=self.rows,
        )
