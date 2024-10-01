from dash import html

percentyle_analysis_headers = [
    "Type",
    "Position",
    "Percentile",
    "Data Set",
    # html.P(
    #     className="mb-0",
    #     children=html.Div(
    #         children=[
    #             html.Div(className="m-0", children="Percentil"),
    #             html.P(
    #                 className='fw-normal m-0 fs-7 text-dark', children="(Last Analysis)"
    #             ),
    #         ]
    #     ),
    # ),
]

ssindex_impact_analysis_headers = [
    html.P(className="text-primary mb-0", children="#"),
    html.P(className="text-primary mb-0", children="Pilar ESG"),
    html.P(className="text-ssindex-graph-grey mb-0", children="No Data"),
    html.P(
        className="text-ssindex-poor mb-0",
        children=html.Div(
            children=[
                html.P(className="m-0", children="Poor"),
                html.P(className='fw-normal m-0 fs-7 text-dark', children="0-19%"),
            ]
        ),
    ),
    html.P(
        className="text-ssindex-low mb-0",
        children=html.Div(
            children=[
                html.P(className="m-0", children="Low"),
                html.P(className='fw-normal m-0 fs-7 text-dark', children="20-39%"),
            ]
        ),
    ),
    html.P(
        className="text-ssindex-average mb-0",
        children=html.Div(
            children=[
                html.P(className="m-0 ", children="Average"),
                html.P(className='fw-normal m-0 fs-7 text-dark', children="40-59%"),
            ]
        ),
    ),
    html.P(
        className="text-ssindex-good mb-0",
        children=html.Div(
            children=[
                html.P(className="m-0", children="Good"),
                html.P(className='fw-normal m-0 fs-7 text-dark', children="60-79%"),
            ]
        ),
    ),
    html.P(
        className="text-ssindex-excellent mb-0",
        children=html.Div(
            children=[
                html.P(className="m-0", children="Excellent"),
                html.P(className='fw-normal m-0 fs-7 text-dark', children="80-100%"),
            ]
        ),
    ),
    "Score",
    html.P(
        className="mb-0",
        children=html.Div(
            children=[
                html.Div(className="m-0", children="Percentil"),
                html.P(
                    className='fw-normal m-0 fs-7 text-dark', children="Local Industry"
                ),
            ]
        ),
    ),
]

data_percentile_analysis = [
    {
        "data": [
            html.P(
                className='text-dark mb-0 d-flex align-items-center fs-7',
                children=[
                    # Blue box beside the text
                    html.Span(
                        className='bg-primary rounded-1',
                        style={"width": "20px", "height": "20px", "min-width": "20px"},
                        children="\u200B",
                    ),
                    # Text
                    "Global Universe",
                ],
            ),
            html.P(
                className='text-ssindex-graph-grey mb-0',
                children=[html.B("5"), " out of 5"],
            ),
            html.B(className='text-ssindex-graph-grey mb-0', children="20th"),
            html.P(className='text-ssindex-graph-grey mb-0', children="100 out of 400"),
            html.B(className='text-ssindex-graph-grey mb-0', children="20th"),
        ]
    },
    {
        "data": [
            html.Div(
                className='text-dark m-0 d-flex align-items-center fs-7',
                children=[
                    html.P(
                        className='text-dark mb-0 d-flex align-items-center fs-7',
                        children=[
                            # Blue box beside the text
                            html.Span(
                                className='bg-secondary rounded-1',
                                style={
                                    "width": "20px",
                                    "height": "20px",
                                    "min-width": "20px",
                                },
                                children="\u200B",
                            ),
                            # Text
                            "Industry, South America",
                        ],
                    ),
                ],
            ),
            html.P(
                className='text-ssindex-graph-grey mb-0',
                children=[html.B("5"), " out of 5"],
            ),
            html.B(className='text-ssindex-graph-grey mb-0', children="20th"),
            html.P(className='text-ssindex-graph-grey mb-0', children="100 out of 400"),
            html.B(className='text-ssindex-graph-grey mb-0', children="20th"),
        ]
    },
    {
        "data": [
            html.P(
                className='text-dark mb-0 d-flex align-items-center fs-7',
                children=[
                    # Blue box beside the text
                    html.Span(
                        className='bg-light rounded-1',
                        style={"width": "20px", "height": "20px", "min-width": "20px"},
                        children="\u200B",
                    ),
                    # Text
                    "Industry, Country",
                ],
            ),
            html.P(
                className='text-ssindex-graph-grey mb-0',
                children=[html.B("5"), " out of 5"],
            ),
            html.B(className='text-ssindex-graph-grey mb-0', children="20th"),
            html.P(className='text-ssindex-graph-grey mb-0', children="100 out of 400"),
            html.B(className='text-ssindex-graph-grey mb-0', children="20th"),
        ]
    },
]

nested_headers = [
    "Review",
    "Sentiment Score",
    "Category",
    "ESG Pilar",
    "Dimension",
    "Territory or State",
    "City",
    "Date",
    "Source",
]
nested_data = [
    [
        html.P(children="I called and called an no one answered the phone"),
        html.P("8%"),
        html.P(className="text-ssindex-poor", children="Poor"),
        html.P("Social External"),
        html.P("Complaints"),
        html.P("New York"),
        html.P("New York"),
        html.P("12/08/23"),
        html.P("Google"),
    ],
    [
        html.P("I called and called an no one answered the phone"),
        html.P("12%"),
        html.P(className="text-ssindex-poor", children="Poor"),
        html.P("Social External"),
        html.P("Complaints"),
        html.P("California"),
        html.P("Los Angeles"),
        html.P("05/07/24"),
        html.P("Instagram"),
    ],
    [
        html.P(
            "I had a problem with one of the products, called, no one answered, then sent an email and the got back to me in two days. Fortunately the problem was solved"
        ),
        html.P("54%"),
        html.P(className='text-ssindex-average', children="Average"),
        html.P("Social External"),
        html.P("Complaints"),
        html.P("Texas"),
        html.P("Houston"),
        html.P("24/04/24"),
        html.P("Facebook"),
    ],
]

data_ssindex_impact_analysis = [
    {
        "data": [
            html.P(className="text-primary mb-0", children="01"),
            html.P(className='text-primary mb-0', children="Environment"),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-average border border-dark border-4 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100  border rounded",
                children=html.B(className='text-white', children="45%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="02"),
            html.P(className='text-primary mb-0', children="Social Capital"),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor border border-dark border-4 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100  border rounded",
                children=html.B(className='text-white', children="15%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="03"),
            html.P(className='text-primary mb-0', children="Human Capital"),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 border border-dark border-4",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-average opacity-40 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100  border rounded",
                children=html.B(className='text-white', children="30%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="04"),
            html.P(
                className='text-primary mb-0',
                children="Business Model & Innovation",
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good border border-dark border-4 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100  border rounded",
                children=html.B(className='text-white', children="65%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="05"),
            html.P(
                className='text-primary mb-0',
                children="Leadership & Governance",
            ),
            html.Div(
                className="bg-ssindex-no-data opacity-40 w-100 h-100", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 border border-dark border-4",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="06"),
            html.P(className='text-primary mb-0', children="Others"),
            html.Div(
                className="bg-ssindex-no-data border border-dark border-4 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
]
