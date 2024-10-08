'''
Table Body Definition
'''

from typing import List, Optional
from DashMonitor.app.views.components.base_component import BaseComponent
from dash import html
from typing import List, Dict, Any, Optional
from DashMonitor.app.views.components.table.table_header import TableHeader


class TableBody(BaseComponent):
    '''
    Table Body component. Generates a tbody for a table.
    '''

    def __init__(
        self,
        data: List[html.Tr] | html.Tr,
        class_name: Optional[str] = '',
        class_name_rows: Optional[str] = '',
    ):
        self.data = data
        self.class_name = class_name
        self.class_name_rows = class_name_rows

    def _render_nested_table(
        self, nested_data: List[List[str]], nested_headers: List[str], index: int
    ) -> html.Tr:
        """
        Renders a nested table inside a collapsible row.

        Parameters
        ----------
        nested_data : List[List[str]]
            A list of lists, where each inner list represents a row of values for the nested table.
        nested_headers : List[str]
            A list of strings representing the headers to display in the nested table.
        index : int
            The index of the row. Used to create unique class names for collapsibility
            and to differentiate nested tables in the DOM.
        """
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
                        className=f'nestedTable{index}',
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
            className=f'collapse nestedTable{index} {self.class_name_rows}',
        )

    def _render_main_row(self, row: Dict[str, Any], index: int) -> html.Tr:
        """
        Renders a single row of the main table and adds collapsibility if nested data is present.

        Parameters
        ----------
        row : Dict[str, Any]
            A dictionary representing the row data. It must contain a key 'data' with a list of values
            for the main table row. If the row has nested data, it may include:
            - 'nested_data': List of lists, where each inner list represents a row of nested table data.
            - 'nested_headers': List of strings for nested table headers (optional).
        index : int
            The index of the row. Used to associate the main row with its corresponding nested table
            for collapsibility.
        """
        return html.Tr(
            className=self.class_name_rows,
            role='button' if 'nested_data' in row else None,
            children=[html.Td(val) for val in row['data']],
            **(
                {
                    'data-bs-toggle': 'collapse',
                    'data-bs-target': f'.nestedTable{index}',
                }
                if 'nested_data' in row
                else {}
            ),
        )

    def _render_rows(self) -> List[html.Tr]:
        """
        Renders all rows for the main table, including nested tables if present.

        This method iterates through the data provided to the table and generates a list of Dash `html.Tr` components, representing each row in the table.
        If a row contains nested data, it will generate both the main row and a collapsible nested table.
        """
        rows = []
        # Loop through each row of data
        for index, row in enumerate(self.data):
            # Create the main row
            main_row = self._render_main_row(row, index)
            # Get the nested headers if present
            nested_headers = row.get('nested_headers', [])
            # Append the main row and the nested table if present
            rows.extend(
                [
                    main_row,
                    self._render_nested_table(
                        row['nested_data'], nested_headers, index
                    ),
                ]
                if 'nested_data' in row
                else [main_row]
            )

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
