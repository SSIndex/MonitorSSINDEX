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
from DashMonitor.app.data.analyzers import GeneralAnalyzer
from DashMonitor.app.handlers.function_utils import (
    categorize_score,
    create_result_table,
    create_gauge_chart,
    create_gauge_chart_ssindex,
)
from DashMonitor.app.handlers import gu
from DashMonitor.app.views.configs import main_df_provider

<<<<<<< HEAD
=======
from DashMonitor.app.views import components as cpt

# Import mock data
from DashMonitor.app.views.layouts.mock_data_sasb_analysis import *
from DashMonitor.app.views.layouts.mock_data_general_analysis import *

category_order = ["Universe", "Industry", "Company"]
custom_colors = {
    "Universe": "#1f77b4",  # Blue
    "Industry": "#2ca02c",  # Green
    "Company": "#ff7f0e",  # Orange
}
>>>>>>> feat/rebase_new

bkn = "Boeing"

analyzer = GeneralAnalyzer(
    main_df_provider,
    None  # Should be the app to register recalculation callbacks
)

df = analyzer.execute()
general_score = analyzer.general_score(bkn)
general_gauge_chart, explanation_general_gauge_chart = create_gauge_chart(general_score)


df1 = main_df_provider()
df_grouped = (
    df1.groupby("state").agg({"Sentiment_score": "mean"}).reset_index()
)
industry_comments = df1[df1["Industry"] == "Aviation & Aerospace."]
industry_comments["Sentiment_Category"] = industry_comments[
    "Sentiment_score"
].apply(categorize_score)
universe_totals = df1["Sentiment_Category"].value_counts(normalize=True) * 100
industry_totals = (
    industry_comments["Sentiment_Category"].value_counts(normalize=True) * 100
)
obj_bank = df1[df1["Bank Name"] == bkn]
total_obj_bank = len(obj_bank)
obj_bank_totals_corrected = (
    obj_bank["Sentiment_Category"].value_counts(normalize=True) * 100
)
percentage_data_corrected = []
for category in gu.CATEGORY_ORDER:
    percentage_data_corrected.append(
        {
            "Category": category,
            "Type": "Universe",
            "Percentage": universe_totals.get(category, 0),
        }
    )
    percentage_data_corrected.append(
        {
            "Category": category,
            "Type": "Industry",
            "Percentage": industry_totals.get(category, 0),
        }
    )
    percentage_data_corrected.append(
        {
            "Category": category,
            "Type": "Company",
            "Percentage": obj_bank_totals_corrected.get(category, 0),
            "Company": "Webster Bank",
        }
    )

percentage_df_corrected = pd.DataFrame(percentage_data_corrected)
percentage_df_corrected["Category"] = pd.Categorical(
    percentage_df_corrected["Category"],
    categories=gu.CATEGORY_ORDER,
    ordered=True,
)
percentage_df_corrected = percentage_df_corrected.sort_values("Category")

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
    uniformtext_minsize=14,
    plot_bgcolor='#E8F4FF',
    paper_bgcolor='#E8F4FF'
)

score_by_pillar = (
    df1.groupby("Predicted_SASB")
    .agg(Avg_Score=("Sentiment_score", "mean"))
    .reset_index()
)
pillars = score_by_pillar["Predicted_SASB"].unique()
# Crear gráficos de medidor para cada pilar

gauge_figures_2 = []

for index, row in score_by_pillar.iterrows():
    score = row["Avg_Score"]
    pillar_name = row["Predicted_SASB"]
    fig = create_gauge_chart_ssindex(score, pillar_name)
    gauge_figures_2.append(
        dbc.Row(
            [
                dbc.Col(
                    html.H4(
                        pillar_name,
                        style={"textAlign": "left", "padding-right": "20px"},
                    ),
                    width=2,
                    style={"display": "flex", "align-items": "center"},
                ),
                dbc.Col(
                    dcc.Graph(figure=fig, config={"displayModeBar": False}),
                    width=10,
                    style={"padding-left": "0px"},
                ),
            ],
            style={"margin-bottom": "0px", "align-items": "center"},
        )
    )

score_by_pillar = (
    df1.groupby("Pilar")
    .agg(Avg_Score=("Sentiment_score", "mean"))
    .reset_index()
)
pillars = score_by_pillar["Pilar"].unique()
gauge_figures_1 = []
for index, row in score_by_pillar.iterrows():
    score = row["Avg_Score"]
    pillar_name = row["Pilar"]
    fig = create_gauge_chart_ssindex(score, pillar_name)
    gauge_figures_1.append(
        dbc.Row(
            [
                dbc.Col(
                    html.H4(
                        pillar_name,
                        style={"textAlign": "left", "padding-right": "20px"},
                    ),
                    width=2,
                    style={"display": "flex", "align-items": "center"},
                ),
                dbc.Col(
                    dcc.Graph(figure=fig, config={"displayModeBar": False}),
                    width=10,
                    style={"padding-left": "0px"},
                ),
            ],
            style={"margin-bottom": "0px", "align-items": "center"},
        )
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
                                            id="histogram", figure=fig_hist_general,
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
        html.Section(
            className="section pt-5",
            children=[
                html.Div(
                    children=[
                        html.H4(
                            className="text-primary",
                            children=['SSINDEX Impact Analysis'],
                        ),
                        html.P(
                            className='text-ssindex-graph-grey',
                            children=[
                                'Stakeholders evaluate how the company is performing according to the Stakeholders Sustainability Index (SSINDEX) methodology'
                            ],
                        ),
                        cpt.Table(
                            headers=ssindex_impact_analysis_headers,
                            data=data_ssindex_impact_analysis,
                            footer_data=footer_data,
                            class_name_headers=class_name_headers,
                            table_title='Overall Score SASB',
                        ).render(),
                    ]
                )
            ],
        ),
    ],
)
