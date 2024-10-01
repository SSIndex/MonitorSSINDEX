"""
GENERAL Analysis Layout
"""

# std imports
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc

# 3rd party imports
from dash import html

# local imports
from DashMonitor.app.data.analyzers import GeneralAnalyzer, GeneralComparisonAnalyzer
from DashMonitor.app.handlers.function_utils import (
    categorize_score,
    create_result_table,
    create_gauge_chart,
    create_gauge_chart_ssindex,
)

from DashMonitor.app.views import components as cpt

# Import mock data
from DashMonitor.app.views.layouts.mock_data_sasb_analysis import *
from DashMonitor.app.views.layouts.mock_data_general_analysis import *
from DashMonitor.app.handlers import gu
from DashMonitor.app.views.configs import main_df_provider


bkn = "Boeing"

analyzer = GeneralAnalyzer(
    main_df_provider, None  # Should be the app to register recalculation callbacks
)

df = analyzer.execute()
general_score = analyzer.general_score(bkn)
general_gauge_chart, explanation_general_gauge_chart = create_gauge_chart(general_score)


comparison_analyzer = GeneralComparisonAnalyzer(
    "Aviation & Aerospace.",
    "Boeing",
    main_df_provider,
    None,  # Should be the app to register recalculation callbacks
)

percentage_df_corrected = comparison_analyzer.execute()

print(percentage_df_corrected.head(100))

fig_hist_general = px.bar(
    percentage_df_corrected,
    x="Category",
    y="Percentage",
    color="Type",
    barmode="group",
    text="Percentage",
    height=400,
    category_orders={"Type": gu.CATEGORY_ORDER},
    color_discrete_map=gu.CUSTOM_COLORS,
)
fig_hist_general.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
fig_hist_general.update_layout(
    uniformtext_minsize=14, plot_bgcolor='#E8F4FF', paper_bgcolor='#E8F4FF'
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
                    company_name,
                    industry,
                    country,
                    company_image,
                    overview,
                    overview_text,
                    cpt.GaugeChart(
                        score=mock_score,
                        score_text=mock_score_text,
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
