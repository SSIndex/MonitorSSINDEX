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
    class_name : Optional[str], default None
        Custom class name to apply to the main table. Defaults to _BASE_CLASS_NAME.
    Data payload example:
    data = [
        {"data": [html.Div("Row 1"), html.Div("Value 1")]},
        {"data": ["Row 2", "Value 2"],
            "nested_data": [["Nested Value 1", "Nested Value 2"], ["Nested Value 3", "Nested Value 4"]],
            "nested_headers": ["Custom Header 1", "Custom Header 2"]},
        {"data": ["Row 3", "Value 3"]},
        {"data": ["Row 4", "Value 4"], "nested_data": [[html.Div("Nested Value 5")]]}
        ]
    """

    _BASE_CLASS_NAME = "table table-bordered table-hover table-responsive"

    def __init__(
        self,
        headers: List[str],
        data: List[Dict[str, Any]],
        class_name: Optional[str] = None,
    ):

        self.headers = headers
        self.data = data
        self.class_name = class_name if class_name else self._BASE_CLASS_NAME

    def _render_nested_table(
        self, nested_data: List[List[str]], nested_headers: List[str], index: int
    ) -> html.Tr:
        '''
        Generates a nested table as a Dash component inside a collapsible row.
        '''
        return html.Tr(
            html.Td(
                colSpan=len(self.headers),
                children=[
                    html.Div(
                        className=f"nestedTable{index}",
                        children=html.Table(
                            className="table table-bordered table-hover table-responsive",
                            children=[
                                html.Thead(
                                    children=[
                                        html.Tr(
                                            children=[
                                                html.Th(header, scope="col")
                                                for header in nested_headers
                                            ]
                                        )
                                    ]
                                ),
                                html.Tbody(
                                    children=[
                                        html.Tr(
                                            children=[
                                                html.Td(val) for val in nested_row
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
            className=f"collapse nestedTable{index}",
        )

    def render(self) -> html.Table:
        '''
        Generates the Dash Component for the main table.
        '''
        rows = []

        # Loop through each row of data
        for index, row in enumerate(self.data):
            # Create the main row
            main_row = html.Tr(
                children=[html.Td(val) for val in row['data']],
                **(
                    {
                        "data-bs-toggle": "collapse",
                        "data-bs-target": f".nestedTable{index}",
                    }
                    if 'nested_data' in row
                    else {}
                ),
            )
            rows.append(main_row)

            # If the row contains nested data, add the nested row immediately after
            if 'nested_data' in row:
                # Nested table headers can be optional
                nested_headers = row.get('nested_headers', [])
                nested_row = self._render_nested_table(
                    row['nested_data'], nested_headers, index
                )
                rows.append(nested_row)

        return html.Table(
            className=self.class_name,
            children=[
                html.Thead(
                    children=[
                        html.Tr(
                            children=[
                                html.Th(header, scope="col") for header in self.headers
                            ]
                        )
                    ]
                ),
                html.Tbody(children=rows),
            ],
        )
