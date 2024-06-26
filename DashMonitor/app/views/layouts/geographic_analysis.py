"""
GEOGRAPHIC Analysis Layout
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
from DashMonitor.app.handlers.function_utils import (
    categorize_score,
    create_result_table,
    create_gauge_chart,
    create_gauge_chart_ssindex,
)

category_order = ["Universe", "Industry", "Company"]
custom_colors = {
    "Universe": "#1f77b4",  # Blue
    "Industry": "#2ca02c",  # Green
    "Company": "#ff7f0e",  # Orange
}

bkn = "Banco de Chile"

#df = pd.read_csv("/app/DashMonitor/data/data_procesa_inferencia_webster_SASB.csv")
df = pd.read_csv("/app/DashMonitor/data/data_sampled_full_chile.csv")
filtro_general = (df["Pilar"] == "Other") & (df["Predicted_SASB"] == "Other")
df = df[filtro_general].reset_index(drop=True)

GEOGRAPHIC_ANALYSIS_LAYOUT = html.Div(
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
                                html.H3(children=["Analisis Geografico Pilar SASB"])
                            ],
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
                                    children=dcc.Graph(id="general-map"),
                                ),
                            ],
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
                                    children=html.Div(id="general-table"),
                                )
                            ],
                        ),
                    ],
                )
            ],
        ),
    ],
)


def register_callbacks(app):
    @app.callback(
        [Output("general-map", "figure"), Output("general-table", "children")],
        [Input("general-map", "clickData")],
    )
    def update_general_map(click_data):
        filtered_df = df.copy()
        filtered_df = filtered_df[filtered_df["Bank Name"] == bkn]
        df_grouped = (
            filtered_df.groupby("state").agg({"Sentiment_Score": "mean"}).reset_index()
        )
        df_grouped["color"] = df_grouped["Sentiment_Score"].apply(
            lambda x: "blue" if x > 0 else "red"
        )

        fig = go.Figure(
            data=go.Choropleth(
                locations=df_grouped["state"],
                z=df_grouped["Sentiment_Score"],
                locationmode="USA-states",
                colorscale="Blues",
                marker_line_color="white",
            )
        )
        fig.update_layout(
            title_text=f"Average Sentiment Score by State for {bkn}",
            geo_scope="usa",
        )
        reviews_table = html.Table()
        if click_data:
            state = click_data["points"][0]["location"]
            reviews = filtered_df[filtered_df["state"] == state][
                ["Review", "Sentiment_Score", "Bank Name"]
            ].head(5)
            reviews_table = html.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th(
                                    col,
                                    style={
                                        "padding": "10px",
                                        "border": "1px solid black",
                                    },
                                )
                                for col in reviews.columns
                            ]
                        )
                    ),
                    html.Tbody(
                        [
                            html.Tr(
                                [
                                    html.Td(
                                        reviews.iloc[i][col],
                                        style={
                                            "padding": "10px",
                                            "border": "1px solid black",
                                        },
                                    )
                                    for col in reviews.columns
                                ]
                            )
                            for i in range(len(reviews))
                        ]
                    ),
                ],
                style={
                    "width": "100%",
                    "borderCollapse": "collapse",
                    "marginTop": "20px",
                },
            )
        return fig, reviews_table


def register_layout_and_callbacks_map(app):
    register_callbacks(app)
