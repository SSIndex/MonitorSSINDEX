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
    th_class_name : Optional[str] | Optional[list[str]]
        Class name to apply to the th elements. It can be a list for each th or a single class to apply to all elements.
    """

    def __init__(
        self,
        headers: List[str],
        thead_class_name: Optional[str] = "",
        th_class_name: Optional[str] | Optional[list[str]] = "",
    ):
        self.thead_class_name = thead_class_name
        self.th_class_name = th_class_name
        self.headers = headers

    def _build_th_class(self, base_class: str, index: int) -> str:
        """
        Builds the class name for a <th> element, adding rounded-start-4 and rounded-end-4
        based on the position (first or last).

        Parameters
        ----------
        base_class : str
            The base class name for the <th>.
        index : int
            The index of the header column.
        """
        class_name = base_class
        if index == 0:
            class_name += ' rounded-start-4'
        if index == len(self.headers) - 1:
            class_name += ' rounded-end-4'
        return class_name

    def _render_th(self) -> List[html.Th]:
        """Render table header cells (th) with class names and rounded styles."""

        th_classes = (
            self.th_class_name
            if isinstance(self.th_class_name, list)
            else [self.th_class_name] * len(self.headers)
        )

        return [
            html.Th(
                header,
                className=self._build_th_class(th_classes[i], i),
                style={
                    'width': (
                        f'{100 / len(self.headers)}%'
                        if not isinstance(self.th_class_name, list)
                        else {}
                    )
                },
            )
            for i, header in enumerate(self.headers)
        ]

    def render(self) -> html.Thead:
        """
        Renders a table-head
        """
        return html.Thead(
            className=self.thead_class_name,
            children=html.Tr(
                className='text-center',
                children=self._render_th(),
            ),
        )
