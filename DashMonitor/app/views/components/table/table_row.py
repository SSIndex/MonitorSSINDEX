from dash import html
from typing import Dict, Any, List, Optional
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
    class_name_td: Optional[list[str]], default None
        Custom class name to apply to the td elements. Defaults to None.
    class_name_nested_table_container : str, default NESTED_TABLE_CONTAINER_TD_CLASS_NAME
        Custom class name to apply to the nested table container td element. Defaults to NESTED_TABLE_CONTAINER_TD_CLASS_NAME.
    class_name_nested_table : str, default NESTED_TABLE_CLASS_NAME
        Custom class name to apply to the nested table. Defaults to NESTED_TABLE_CLASS_NAME.

    """

    NESTED_TABLE_CONTAINER_TD_CLASS_NAME = (
        'table-ssindex-nested-table-background text-center rounded-3 shadow-none'
    )
    NESTED_TABLE_CLASS_NAME = 'table table-borderless table-responsive table-ssindex-nested-table-background rounded'
    NESTED_TABLE_TH_CLASS_NAME = 'text-center table-white fs-7'
    NESTED_TABLE_TD_CLASS_NAME = 'text-center align-middle fs-7'

    def __init__(
        self,
        row_data: Dict[str, Any],
        index: int,
        class_name_rows: str = '',
        class_name_td: Optional[list[str]] = None,
        class_name_nested_table_container: str = NESTED_TABLE_CONTAINER_TD_CLASS_NAME,
        class_name_nested_table: str = NESTED_TABLE_CLASS_NAME,
    ):
        self.row_data = row_data
        self.index = index
        self.class_name_rows = class_name_rows
        self.class_name_td = (
            class_name_td if class_name_td else [''] * len(row_data['data'])
        )
        self.class_name_nested_table_container = class_name_nested_table_container
        self.class_name_nested_table = class_name_nested_table
        self.nested_data = row_data.get('nested_data', [])
        self.nested_headers = row_data.get('nested_headers', [])

    def _render_nested_table(self) -> html.Tr:
        """
        Renders a nested table inside a collapsible row.
        It assumes that the first Th/Td element of the row must be aligned to the left.
        """
        rows = [
            html.Tr(
                children=[
                    html.Td(
                        className=(
                            self.NESTED_TABLE_TD_CLASS_NAME
                            if index != 0
                            else 'text-start align-middle fs-7'
                        ),
                        children=val,
                    )
                    for index, val in enumerate(nested_row)
                ]
            )
            for nested_row in self.nested_data
        ]

        first_th_class_name = [
            f'text-start table-white fs-7 w-{len(self.nested_headers)}'
        ]
        rest_th_class_name = [
            self.NESTED_TABLE_TH_CLASS_NAME + f" w-{len(self.nested_headers)}"
        ] * (len(self.nested_headers) - 1)
        th_class_name = first_th_class_name + rest_th_class_name

        return html.Tr(
            children=html.Td(
                className=self.class_name_nested_table_container,
                colSpan=100,
                children=[
                    html.Div(
                        className=f'nestedTable{self.index}',
                        children=html.Table(
                            className=self.class_name_nested_table,
                            children=[
                                TableHeader(
                                    headers=self.nested_headers,
                                    th_class_name=th_class_name,
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
        Applies class names to each td.
        """
        return html.Tr(
            className=self.class_name_rows,
            style={'height': '60px'},
            role='button' if self.nested_data else None,
            # Apply class_name_td to each <td> based on the index
            children=[
                html.Td(val, className=self.class_name_td[i])
                for i, val in enumerate(self.row_data['data'])
            ],
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
