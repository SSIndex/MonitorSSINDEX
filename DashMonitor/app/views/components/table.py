'''
Table Class Definition.
'''

from typing import List, Dict, Any, Optional

from dash import html


class Table:
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
        Custom class name to aply to main table headers. Defaults to an empty string.
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
        class_name_table: Optional[str] = None,
        class_name_headers: Optional[str] = None,
        class_name_rows: Optional[str] = None,
        class_name_div: Optional[str] = None,
    ):
        self.table_title = table_title
        self.headers = headers
        self.data = data
        self.footer_data = footer_data
        self.class_name_table = (
            class_name_table if class_name_table else self._BASE_CLASS_NAME
        )
        self.class_name_headers = class_name_headers if class_name_headers else ''
        self.class_name_rows = class_name_rows if class_name_rows else ''
        self.class_name_div = (
            class_name_div if class_name_div else self._BASE_DIV_CLASS_NAME
        )

    def _render_table_headers(self, header_class_name: str, headers: List[str]) -> html.Tr:
        """
        Generates a table header row. 
        
        Parameters
        ----------
        header_class_name : str
            The class name to be applied to each `html.Th` element in the header row. Allows for custom styling of the header.
        headers : List[str]
            A list of strings representing the headers to display in the table.
        """
        return html.Tr(
            className='text-center',
            children=[
                html.Th(
                    header,
                    className=(
                        f'{header_class_name}' +
                        (' rounded-start-4' if i == 0 else '') +
                        (' rounded-end-4' if i == len(headers) - 1 else '')
                    ),
                    style={'width': f'{100 / len(headers)}%'},
                )
                for i, header in enumerate(headers)
            ]
        )

    def _render_nested_table(
        self, nested_data: List[List[str]], nested_headers: List[str], index: int
    ) -> html.Tr:
        '''
        Generates a nested table as a Dash component inside a collapsible row.
        '''
        return html.Tr(
            children=html.Td(
                className='table-ssindex-nested-table-background text-center rounded-3',
                style={'box-shadow': 'none'},
                colSpan=len(self.headers),
                children=[
                    html.Div(
                        className=f'nestedTable{index}',
                        children=html.Table(
                            className='table table-borderless table-responsive table-ssindex-nested-table-background rounded',
                            children=[
                                html.Thead(
                                    className='text-center table-white align-middle',
                                    children=[
                                        self._render_table_headers(header_class_name='text-center table-white fs-7', headers=nested_headers)
                                    ],
                                ),
                                html.Tbody(
                                    children=[
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
                                ),
                            ],
                        ),
                    )
                ],
            ),
            className=f'collapse nestedTable{index} {self.class_name_rows}',
        )
    
    def _render_main_row(self, row: Dict[str, Any], index: int) -> html.Tr:
        """
        Renders the main row of the main table. It also adds the necessary attributes to make the row collapsible if it contains nested data.
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
            rows.extend([main_row, self._render_nested_table(row['nested_data'], nested_headers, index)] if 'nested_data' in row else [main_row])

        return rows
    
    def _render_footer(self) -> html.Tfoot:
        '''
        Generates the tabler footer if footer_data is present.
        '''
        return html.Tfoot(
            className='border-top text-center',
            children=[
                html.Tr(
                    children=[
                        (
                            html.Th(val) if i == 0
                            else html.Td(val, className='text-center')
                        )
                        for i, val in enumerate(self.footer_data)
                    ]
                )
            ],
        ) if self.footer_data else None

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
                        html.Thead(
                            className='text-center align-middle',
                            children=[
                                self._render_table_headers(header_class_name=self.class_name_headers, headers=self.headers)
                            ],
                        ),
                        html.Tbody(className="align-middle text-center", children=rows),
                        self._render_footer(),
                    ],
                ),
            ],
        )
