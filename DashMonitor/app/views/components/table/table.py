'''
Table Class Definition.
'''

from typing import List, Dict, Any, Optional
from DashMonitor.app.views.components.base_component import BaseComponent
from dash import html

from DashMonitor.app.views.components.table.table_body import TableBody
from DashMonitor.app.views.components.table.table_header import TableHeader
from DashMonitor.app.views.components.table.table_footer import TableFooter


class Table(BaseComponent):
    """
    Table Component. Generates a table with the given headers, data, and class name, supporting optional collapsible nested tables.

    Parameters
    ----------
    headers : List[str]
        List of table headers for the main table. Example: ['Pilar 1', 'Pilar 2'].
    data : List[Dict[str, Any]]
        List of dictionaries where each dictionary represents a row in the table.
        Each dictionary must contain a key 'data' with a list of values corresponding to the main table's row data.
        Optionally, a dictionary can contain:
        - 'nested_headers': List of strings representing headers for the nested table (if present).
          Example: 'nested_headers': ['Nested Header 1', 'Nested Header 2']
        - 'nested_data': List of lists, where each inner list represents a row of data for the nested table.
          Example: 'nested_data': [['Nested Value 1', 'Nested Value 2']]
    footer_data : List[str]
        List of values to display in the footer row of the table. Example: ['Total', 'Value 1', 'Value 2']. Empty strings can be used to omit columns
    table_title : Optional[str], default ''
        Title to display above the table. Defaults to an empty string.
    class_name_table : Optional[str], default None
        Custom class name to apply to the main table. Defaults to _BASE_CLASS_NAME.
    class_name_headers : Optional[str], default None
        Custom class name to aply to main table headers (Th elements). Defaults to an empty string.
    class_name_rows : Optional[str], default None
        Custom class name to apply to main table rows. Defaults to an empty string.
    class_name_div : Optional[str], default None
        Custom class name to apply to the div containing the table. Defaults to _BASE_DIV_CLASS_NAME.

    Data payload example:
    data = [
        {"data": [html.Div("Value 1"), html.Div("Value 2")]},
        {"data": ["Value 3", "Value 4"],
        "nested_data": [
            ["Nested Value 1", "Nested Value 2"],
            ["Nested Value 3", "Nested Value 4"]],
        "nested_headers": ["Custom Header 1", "Custom Header 2"]},
        {"data": ["Value 5", "Value 6"]},
        {"data": ["Value 7", "Value 8"], "nested_data": [[html.Div("Nested Value 5")]]},
        ]
    """

    _BASE_CLASS_NAME = 'table table-borderless table-responsive table-hover mt-4'
    _BASE_DIV_CLASS_NAME = 'bg-white rounded rounded-4 p-3 shadow-sm'

    def __init__(
        self,
        headers: List[str],
        data: List[Dict[str, Any]],
        footer_data: Optional[List[str]] = [],
        table_title: Optional[str] = '',
        class_name_table: Optional[str] = _BASE_CLASS_NAME,
        class_name_headers: Optional[str] = '',
        class_name_rows: Optional[str] = '',
        class_name_div: Optional[str] = _BASE_DIV_CLASS_NAME,
    ):
        self.table_title = table_title
        self.headers = headers
        self.data = data
        self.footer_data = footer_data
        self.class_name_table = class_name_table
        self.class_name_headers = class_name_headers
        self.class_name_rows = class_name_rows
        self.class_name_div = class_name_div

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
                colSpan=len(self.headers),
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
                                TableBody(
                                    rows=rows,
                                ).render(),
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

    def render(self) -> html.Table:
        '''
        Generates the Dash Component for the table.
        '''
        rows = self._render_rows()
        return html.Div(
            className=self.class_name_div,
            children=[
                html.H5(className='text-primary', children=f'{self.table_title}'),
                html.Table(
                    className=self.class_name_table,
                    children=[
                        TableHeader(
                            headers=self.headers,
                            thead_class_name='text-center align-middle',
                            th_class_name=self.class_name_headers,
                        ).render(),
                        TableBody(
                            rows=rows, class_name="align-middle text-center"
                        ).render(),
                        TableFooter(self.footer_data).render(),
                    ],
                ),
            ],
        )