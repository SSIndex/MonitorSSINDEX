from typing import List, Dict, Any, Optional

from dash import html, callback
import dash_core_components as dcc

from DashMonitor.app.views.components.base_component import BaseComponent

from dash.dependencies import Input, Output, State


class Table(BaseComponent):
    """
    Table Component. Generates a table with the given data.
    """

    BASE_CLASS_NAME = "table table-bordered table-hover table-responsive mt-4"

    def __init__(self, headers: List[str], data: List[List[str]], class_name=Optional[str], is_nested=False):
        self.headers = headers
        self.data = data
        self.class_name = class_name if class_name else self.BASE_CLASS_NAME
        print("self.class_name:", self.class_name)

        print("self.headers:", self.headers)
        print("self.data:", self.data)
        for row in self.data:
            print("row:", row)

    def render(self) -> html.Table:
        """
        Render the Table Component.
        """
        # return html.Table(
        #     className=self.BASE_CLASS_NAME,
        #     children=[
        #         html.Thead(
        #             children=[
        #                 html.Tr(
        #                     children=[
        #                         html.Th(header, scope='col') for header in self.headers
        #                     ]
        #                 )
        #             ]
        #         ),
        #         html.Tbody(
        #             children=[
        #                 html.Tr(
        #                     children=[
        #                         html.Td(val) for val in row
        #                     ]
        #                 ) for row in self.data
        #             ]
        #         )
        #     ]
        # )
        # Example hardcoded table
        return html.Table(
            className="table table-bordered table-hover table-responsive mt-4",
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
                html.Tbody(
                    children=[
                        html.Tr(
                            children=[
                                # Bootstrap Collapse Button using data-bs-toggle
                                html.Td(
                                        "1",
                                        # **{
                                        #     "data-bs-toggle": "collapse",
                                        #     "data-bs-target": "#nestedTable",
                                        # }

                                ),
                                html.Td("2"),
                            ],
                            **{
                                "data-bs-toggle": "collapse",
                                "data-bs-target": "#nestedTable",
                            }
                        ),
                        # Nested table with collapse functionality
                        html.Tr(
                            html.Td(
                                colSpan="2",  # Span across two columns
                                children=[
                                    html.Div(
                                        id="nestedTable",
                                        className="collapse",  # Bootstrap collapse class
                                        children=[
                                            html.Table(
                                                className="table table-bordered table-hover table-responsive mt-4",
                                                children=[
                                                    html.Thead(
                                                        children=[
                                                            html.Tr(
                                                                children=[
                                                                    html.Th(
                                                                        "Pilar 1a",
                                                                        scope="col",
                                                                    ),
                                                                    html.Th(
                                                                        "Pilar 2a",
                                                                        scope="col",
                                                                    ),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                    html.Tbody(
                                                        children=[
                                                            html.Tr(
                                                                children=[
                                                                    html.Td("1"),
                                                                    html.Td("2"),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ],
                                            )
                                        ],
                                    )
                                ],
                            )
                        ),
                        html.Tr(
                            children=[
                                html.Td("4"),
                                html.Td("5"),
                            ]
                        )
                    ]
                ),
            ],
        )