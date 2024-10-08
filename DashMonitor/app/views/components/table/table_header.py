'''
Table Header Class definition
'''

from dash import html

from typing import List, Optional

from DashMonitor.app.views.components.base_component import BaseComponent


class TableHeader(BaseComponent):
    """
    Table Header component. Generates a thead for a table.

    Parameters
    ----------
    headers : List[str]
        List of table headers to display.
    thead_class_name : Optional[str]
        Class name to apply to the thead element.
    th_class_name : Optional[str]
        Class name to apply to the th elements.
    """

    def __init__(
        self,
        headers: List[str],
        thead_class_name: Optional[str] = "",
        th_class_name: Optional[str] = "",
    ):
        self.thead_class_name = thead_class_name
        self.th_class_name = th_class_name
        self.headers = headers

    def render(self) -> html.Thead:
        """
        Renders a table-head
        """
        return html.Thead(
            className=self.thead_class_name,
            children=html.Tr(
                className='text-center',
                children=[
                    html.Th(
                        header,
                        className=(
                            f'{self.th_class_name}'
                            + (' rounded-start-4' if i == 0 else '')
                            + (' rounded-end-4' if i == len(self.headers) - 1 else '')
                        ),
                        style={'width': f'{100 / len(self.headers)}%'},
                    )
                    for i, header in enumerate(self.headers)
                ],
            ),
        )
