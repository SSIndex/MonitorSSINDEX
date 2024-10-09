from dash import html
from typing import Dict, Any, List
from DashMonitor.app.views.components.table.table_header import TableHeader


class TableRow:
    """
    TableRow component. Generates either a main or nested table row.

    Parameters
    ----------
    row_data : Dict[str, Any]
        Dictionary containing the row data.
    index : int
        Index of the row.
    class_name_rows : str, default ''
        Custom class name to apply to the row. Defaults to an empty string.
    """

    NESTED_TABLE_CONTAINER_TD_CLASS_NAME = (
        'table-ssindex-nested-table-background text-center rounded-3 shadow-none'
    )
    NESTED_TABLE_CLASS_NAME = 'table table-borderless table-responsive table-ssindex-nested-table-background rounded'
    NESTED_TABLE_TH_CLASS_NAME = 'text-center table-white fs-7'
    NESTED_TABLE_TD_CLASS_NAME = 'text-center align-middle fs-7'

    def __init__(self, row_data: Dict[str, Any], index: int, class_name_rows: str = ''):
        self.row_data = row_data
        self.index = index
        self.class_name_rows = class_name_rows
        self.nested_data = row_data.get('nested_data', [])
        self.nested_headers = row_data.get('nested_headers', [])

    def _render_nested_table(self) -> html.Tr:
        """
        Renders a nested table inside a collapsible row.
        """
        rows = [
            html.Tr(
                children=[
                    html.Td(
                        className=self.NESTED_TABLE_TD_CLASS_NAME,
                        children=val,
                    )
                    for val in nested_row
                ]
            )
            for nested_row in self.nested_data
        ]

        return html.Tr(
            children=html.Td(
                className=self.NESTED_TABLE_CONTAINER_TD_CLASS_NAME,
                colSpan=100,
                children=[
                    html.Div(
                        className=f'nestedTable{self.index}',
                        children=html.Table(
                            className=self.NESTED_TABLE_CLASS_NAME,
                            children=[
                                TableHeader(
                                    headers=self.nested_headers,
                                    th_class_name=self.NESTED_TABLE_TH_CLASS_NAME,
                                ).render(),
                                html.Tbody(children=rows),
                            ],
                        ),
                    )
                ],
            ),
            className=f'collapse nestedTable{self.index} {self.class_name_rows}',
        )

    def _render_main_row(self) -> html.Tr:
        """
        Renders a single row of the main table and adds collapsibility if nested data is present.
        """
        return html.Tr(
            className=self.class_name_rows,
            role='button' if self.nested_data else None,
            children=[html.Td(val) for val in self.row_data['data']],
            **(
                {
                    'data-bs-toggle': 'collapse',
                    'data-bs-target': f'.nestedTable{self.index}',
                }
                if self.nested_data
                else {}
            ),
        )

    def render(self) -> List[html.Tr]:
        """
        Renders the table row(s). Returns the main row and, if present, the nested table row.
        """
        rows = [self._render_main_row()]
        if 'nested_data' in self.row_data:
            rows.append(self._render_nested_table())
        return rows
