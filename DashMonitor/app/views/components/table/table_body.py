from typing import List, Dict, Any, Optional
from DashMonitor.app.views.components.base_component import BaseComponent
from dash import html
from DashMonitor.app.views.components.table.table_header import TableHeader
from DashMonitor.app.views.components.table.table_row import (
    TableRow,
)  # Import the new component


class TableBody(BaseComponent):
    """
    Table Body component. Generates a tbody for a table.

    Parameters
    ----------
    data : List[Dict[str, Any]]
        List of dictionaries where each dictionary represents a row in the table.
        Each dictionary must contain a key 'data' with a list of values corresponding to the main table's row data.
        Optionally, a dictionary can contain:
        - 'nested_headers': List of strings representing headers for the nested table (if present).
          Example: 'nested_headers': ['Nested Header 1', 'Nested Header 2']
        - 'nested_data': List of lists, where each inner list represents a row of data for the nested table.
          Example: 'nested_data': [['Nested Value 1', 'Nested Value 2']]
    class_name_td: Optional[list[str]], default None
        Custom class name to apply to the td elements. Defaults to None.
    class_name_nested_table_container : str, default NESTED_TABLE_CONTAINER_TD_CLASS_NAME
        Custom class name to apply to the nested table container td element. Defaults to NESTED_TABLE_CONTAINER_TD_CLASS_NAME.
    class_name_nested_table : str, default NESTED_TABLE_CLASS_NAME
        Custom class name to apply to the nested table. Defaults to NESTED_TABLE_CLASS_NAME.
    """

    def __init__(
        self,
        data: List[Dict[str, Any]],
        class_name: Optional[str] = '',
        class_name_rows: Optional[str] = '',
        class_name_td: Optional[list[str]] = None,
        class_name_nested_table_container: str = TableRow.NESTED_TABLE_CONTAINER_TD_CLASS_NAME,
        class_name_nested_table: str = TableRow.NESTED_TABLE_CLASS_NAME,
    ):
        self.data = data
        self.class_name = class_name
        self.class_name_rows = class_name_rows
        self.class_name_td = class_name_td
        self.class_name_nested_table_container = class_name_nested_table_container
        self.class_name_nested_table = class_name_nested_table

    def _render_rows(self) -> List[html.Tr]:
        """
        Renders all rows for the main table, including nested tables if present.
        """
        rows = []
        for index, row in enumerate(self.data):
            table_row = TableRow(
                row_data=row,
                index=index,
                class_name_rows=self.class_name_rows,
                class_name_td=self.class_name_td,
                class_name_nested_table_container=self.class_name_nested_table_container,
                class_name_nested_table=self.class_name_nested_table,
            )
            rows.extend(table_row.render())
        return rows

    def render(self) -> html.Tbody:
        """
        Renders the table body.
        """
        rows = self._render_rows()
        return html.Tbody(
            className=self.class_name,
            children=rows,
        )
