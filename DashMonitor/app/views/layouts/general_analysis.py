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
        html.Section(
            className="section bg-light pt-3",
            children=[
                html.Div(
                    className="container border-bottom border-dark",
                    children=[
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-12 justify-content-end",
                                    children=[
                                        html.P(
                                            children=[
                                                "2024-06-12"
                                            ]  # Here Goes the Date of last data extracted
                                        )
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-6",
                                    children=[
                                        html.Div(
                                            className="row",
                                            children=[
                                                html.H4(children=[bkn])
                                            ],  # Here goes Company Name
                                        ),
                                        html.Div(
                                            className="row",
                                            children=[
                                                html.P(
                                                    children=[
                                                        "Bank | EEUU | Market Name"
                                                    ]
                                                )
                                            ],  # Here goes Company Details
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="col-6",
                                    children=[
                                        dcc.Graph(
                                            id="gauge-chart", figure=general_gauge_chart
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
            className="section bg-white pt-3",
            children=[
                html.Div(
                    className="container border-bottom border-dark",
                    children=[
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-2",
                                    children=[
                                        html.H6(
                                            className="text-end",
                                            children=["ESG COMPASS Overview:"],
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="col-10",
                                    children=[
                                        html.P(
                                            className="text-center",
                                            children=[explanation_general_gauge_chart],
                                        )  # Here goes the overview description
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-6",
                                    children=[
                                        dcc.Graph(
                                            id="histogram", figure=fig_hist_general
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="col-6",
                                    children=[
                                        create_result_table(df1),
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        html.Section(
            className="section bg-light pt-3",
            children=[
                html.Div(
                    className="container border-bottom border-dark",
                    children=[
                        html.Div(
                            className="row",
                            children=[html.H3(children=["Analisis SASB"])],
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-12",
                                    style={
                                        "display": "flex",
                                        "flexDirection": "column",
                                        "alignItems": "stretch",
                                    },
                                    children=gauge_figures_2,
                                )
                            ],
                        ),
                    ],
                )
            ],
        ),
        html.Section(
            className="section bg-light pt-3",
            children=[
                html.Div(
                    className="container border-bottom border-dark",
                    children=[
                        html.Div(
                            className="row",
                            children=[html.H3(children=["Analisis SSINDEX"])],
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-12",
                                    style={
                                        "display": "flex",
                                        "flexDirection": "column",
                                        "alignItems": "stretch",
                                    },
                                    children=gauge_figures_1,
                                )
                            ],
                        ),
                    ],
                )
            ],
        ),
        html.Section(
            className="section bg-light pt-3",
            children=[
                html.Div(
                    className="container border-bottom border-dark",
                    children=[
                        "Analisis Detallado SASB",
                        "Columnas: Dimension | Porcentaje Comentarios del Pilar con respecto a Total | Puntaje | Categorizacion",
                    ],
                )
            ],
        ),
        html.Section(
            className="section bg-white pt-3",
            children=[
                html.Div(
                    className="container border-bottom border-dark",
                    children=[
                        "Analisis Detallado SSINDEX",
                        "Mismos comentarios de Analisis detallado SASB",
                    ],
                )
            ],
        ),
    ],
)
