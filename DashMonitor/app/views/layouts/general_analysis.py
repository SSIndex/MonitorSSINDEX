"""
GENERAL Analysis Layout
"""

# std imports
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc

# 3rd party imports
from dash import html

# local imports
from DashMonitor.app.data.analyzers import (
    GeneralAnalyzer,
    GeneralComparisonAnalyzer,
    SASBAnalyzer,
)
from DashMonitor.app.handlers.function_utils import categorize_score
from DashMonitor.app.handlers import gu
from DashMonitor.app.views import components as cpt
from DashMonitor.app.views.configs import (
    main_df_provider,
    COMPANY_NAME,
    INDUSTRY_NAME,
    COUNTRY,
)

# Import mock data
from DashMonitor.app.views.layouts.mock_data_sasb_analysis import *
from DashMonitor.app.views.layouts.mock_data_general_analysis import *


analyzer = GeneralAnalyzer(
    main_df_provider, None  # Should be the app to register recalculation callbacks
)

num_comments, _ = analyzer.size()
analyzer.execute()
general_score = analyzer.general_score(COMPANY_NAME)


data_percentile_analysis = [
    {
        "data": [
            html.P(
                className='text-dark mb-0 d-flex align-items-center fs-7 gap-1',
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
                children=[html.B("1"), " out of 1"],
            ),
            html.B(className='text-ssindex-graph-grey mb-0', children="100th"),
            html.P(
                className='text-ssindex-graph-grey mb-0',
                children=f"{num_comments} out of {num_comments}",
            ),
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
                children=[html.B("1"), " out of 1"],
            ),
            html.B(className='text-ssindex-graph-grey mb-0', children="100th"),
            html.P(
                className='text-ssindex-graph-grey mb-0',
                children=f"{num_comments} out of {num_comments}",
            ),
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
                    f"{INDUSTRY_NAME.replace('.', '')}, {COUNTRY}",
                ],
            ),
            html.P(
                className='text-ssindex-graph-grey mb-0',
                children=[html.B("1"), " out of 1"],
            ),
            html.B(className='text-ssindex-graph-grey mb-0', children="100th"),
            html.P(
                className='text-ssindex-graph-grey mb-0',
                children=f"{num_comments} out of {num_comments}",
            ),
        ]
    },
]


comparison_analyzer = GeneralComparisonAnalyzer(
    INDUSTRY_NAME,
    COMPANY_NAME,
    main_df_provider,
    None,  # Should be the app to register recalculation callbacks
)

percentage_df_corrected = comparison_analyzer.execute()

fig_hist_general = px.bar(
    percentage_df_corrected,
    x="Category",
    y="Percentage",
    color="Type",
    barmode="group",
    text="Percentage",
    height=600,
    category_orders={"Type": gu.CATEGORY_ORDER},
    color_discrete_map=gu.custom_colors(INDUSTRY_NAME, COMPANY_NAME),
)
fig_hist_general.update_layout(
    uniformtext_minsize=14,
    plot_bgcolor='#E8F4FF',
    paper_bgcolor='#E8F4FF',
    barcornerradius=25,
    yaxis_title="",
    xaxis_title="",
    legend_title="",
    legend=dict(
        orientation="h",  # Horizontal orientation
        yanchor="bottom",  # Anchor the legend to the bottom
        y=-0.2,  # Place the legend slightly below the chart
        xanchor="center",  # Center the legend
        x=0.5,
    ),
)

# Update layout and styling for the text
fig_hist_general.update_traces(
    texttemplate='%{text:.0f}%',  # Format the text to display no decimals (whole numbers)
    textposition='outside',  # Adjust text position (optional)
    textfont=dict(
        family="Manrope",
        size=14,  # Set font size
        color="#333B69",  # Set text color
        weight='bold',  # Make text bold
    ),
)

# ------------------------------------------------------------------------------
GENERAL_ANALYSIS_LAYOUT = html.Div(
    className="container",
    children=[
        # Date Picker Section
        html.Section(
            className='section pt-3 d-flex justify-content-end',
            children=[cpt.DatePicker().render()],
        ),
        # Company Card Section
        html.Section(
            className='section pt-3',
            children=[
                cpt.Card(
                    company_name=COMPANY_NAME,
                    industry=INDUSTRY_NAME,
                    country=COUNTRY,
                    overview=categorize_score(general_score),
                    overview_graph=cpt.GaugeChart(
                        score=general_score,
                        score_text=categorize_score(general_score),
                        min_value=mock_min_value,
                        max_value=mock_max_value,
                        labels=mock_labels,
                        score_labels=mock_score_labels,
                    ).render(),
                ).render(),
            ],
        ),
        # Percentile Analysis Section
        html.Section(
            className="section pt-3 container",
            children=[
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="p-3 col bg-secondary text-white rounded-3",
                            children=[
                                html.H5(children=["Percentile Analysis"]),
                                html.P(
                                    children=[
                                        "The result of the company in analysis is benchmarked with three groups of data:"
                                    ]
                                ),
                                html.Ol(
                                    children=[
                                        html.Li(
                                            children=[
                                                html.B("GLOBAL UNIVERSE"),
                                                ", includes a sample of companies of different industries and countries, worldwide.",
                                            ]
                                        ),
                                        html.Li(
                                            children=[
                                                html.B("INDUSTRY IN REGION"),
                                                ", includes a sample of companies of the same industry and geographical region where the company in analysis is located.",
                                            ]
                                        ),
                                        html.Li(
                                            children=[
                                                html.B("INDUSTRY IN COUNTRY"),
                                                ", includes a benchmark of companies of the same industry and in the same country where the company in analysis is located.",
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        html.Div(
                            className="col",
                            children=[
                                cpt.Table(
                                    headers=percentyle_analysis_headers,
                                    data=data_percentile_analysis,
                                    class_name_headers=class_name_headers,
                                ).render()
                            ],
                        ),
                    ],
                )
            ],
        ),
        # Performance Analysis Section
        html.Section(
            className="section pt-3",
            children=[
                html.H5(children=["Performance Analysis"]),
                html.P(
                    children=[
                        "The results of the company in analysis are classified in a 5-category ratio and benchmarked with three groups of data."
                    ]
                ),
            ],
        ),
        html.Section(
            className="section pt-3",
            children=[
                html.Div(
                    className="container border-bottom border-dark",
                    children=[
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-12",
                                    children=[
                                        dcc.Graph(
                                            id="histogram",
                                            figure=fig_hist_general,
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        html.Section(
            className="section pt-3",
            children=[
                html.Div(
                    children=[
                        html.H4(
                            className="text-primary", children=['SASB Impact Analysis']
                        ),
                        html.P(
                            className='text-ssindex-graph-grey',
                            children=[
                                'Stakeholders evaluate how the company is performing according to the Sustainability Accounting Standards Board (SASB) methodology'
                            ],
                        ),
                        cpt.Table(
                            headers=headers,
                            data=data,
                            footer_data=footer_data,
                            class_name_headers=class_name_headers,
                            table_title='Overall Score SASB',
                        ).render(),
                    ]
                )
            ],
        ),
        # html.Section(
        #     className="section pt-5",
        #     children=[
        #         html.Div(
        #             children=[
        #                 html.H4(
        #                     className="text-primary",
        #                     children=['SSINDEX Impact Analysis'],
        #                 ),
        #                 html.P(
        #                     className='text-ssindex-graph-grey',
        #                     children=[
        #                         'Stakeholders evaluate how the company is performing according to the Stakeholders Sustainability Index (SSINDEX) methodology'
        #                     ],
        #                 ),
        #                 cpt.Table(
        #                     headers=ssindex_impact_analysis_headers,
        #                     data=data_ssindex_impact_analysis,
        #                     footer_data=footer_data,
        #                     class_name_headers=class_name_headers,
        #                     table_title='Overall Score SASB',
        #                 ).render(),
        #             ]
        #         )
        #     ],
        # ),
    ],
)
