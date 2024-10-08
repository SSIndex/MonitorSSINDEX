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

    def __init__(self, row_data: Dict[str, Any], index: int, class_name_rows: str = ''):
        self.row_data = row_data
        self.index = index
        self.class_name_rows = class_name_rows

    def _render_nested_table(self) -> html.Tr:
        """
        Renders a nested table inside a collapsible row.
        """
        nested_data = self.row_data.get('nested_data', [])
        nested_headers = self.row_data.get('nested_headers', [])

        rows = [
            html.Tr(
                children=[
                    html.Td(
                        className="text-center align-middle fs-7",
                        children=val,
                    )
                    for val in nested_row
                ]
            )
            for nested_row in nested_data
        ]

        return html.Tr(
            children=html.Td(
                className='table-ssindex-nested-table-background text-center rounded-3 shadow-none',
                colSpan=100,
                children=[
                    html.Div(
                        className=f'nestedTable{self.index}',
                        children=html.Table(
                            className='table table-borderless table-responsive table-ssindex-nested-table-background rounded',
                            children=[
                                TableHeader(
                                    headers=nested_headers,
                                    thead_class_name='text-center table-white align-middle',
                                    th_class_name='text-center table-white fs-7',
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
            role='button' if 'nested_data' in self.row_data else None,
            children=[html.Td(val) for val in self.row_data['data']],
            **(
                {
                    'data-bs-toggle': 'collapse',
                    'data-bs-target': f'.nestedTable{self.index}',
                }
                if 'nested_data' in self.row_data
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
