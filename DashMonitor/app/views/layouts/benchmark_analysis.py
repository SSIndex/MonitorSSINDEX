"""
BENCHMARK Analysis Layout
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
df1 = df.copy()
filtro_general = (df["Pilar"] == "Other") & (df["Predicted_SASB"] == "Other")
df = df[filtro_general].reset_index(drop=True)
df = (
    df.groupby(["Bank Name", "Predicted_Pilar", "year", "month_num"])[
        ["Normalized_Sentiment_Score"]
    ]
    .mean()
    .reset_index()
)
df["date"] = pd.to_datetime(
    df["year"].astype(str) + "-" + df["month_num"].map("{:02}".format), format="%Y-%m"
)
df["Total_Sentiment_Score"] = df.groupby(["Bank Name", "date"])[
    "Normalized_Sentiment_Score"
].transform("mean")
df.sort_values("date", inplace=True)

from dash import html

# Your imports and code...

BENCHMARK_ANALYSIS_LAYOUT = html.Div(
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
                                        dcc.Dropdown(
                                            id="year-dropdown",
                                            options=[
                                                {"label": str(year), "value": year}
                                                for year in df["year"].unique()
                                            ],
                                            value=df["year"].max(),
                                            clearable=False,
                                        ),
                                        dcc.Dropdown(
                                            id="pilar-dropdown",
                                            options=[
                                                {"label": pilar, "value": pilar}
                                                for pilar in df[
                                                    "Predicted_Pilar"
                                                ].unique()
                                            ],
                                            value=df["Predicted_Pilar"].unique()[0],
                                            clearable=False,
                                        ),
                                        dcc.Dropdown(
                                            id="bank-dropdown",
                                            options=[
                                                {"label": bank, "value": bank}
                                                for bank in df["Bank Name"].unique()
                                            ],
                                            value=df["Bank Name"].unique()[2],
                                            clearable=False,
                                        ),
                                        dcc.Checklist(
                                            id="bank-checklist",
                                            options=[
                                                {"label": name, "value": name}
                                                for name in df["Bank Name"].unique()
                                            ],
                                            value=["Webster Bank"],
                                            inline=False,
                                            style={
                                                "display": "flex",
                                                "flex-direction": "column",
                                                "gap": "10px",
                                            },
                                        ),
                                    ],
                                    style={"padding": "20px"},
                                ),
                            ],
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-4",
                                    children=[dcc.Graph(id="boxplot-chart")],
                                ),
                                html.Div(
                                    className="col-8",
                                    children=[dcc.Graph(id="overall-time-line-plot")],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


def register_callbacks(app):
    @app.callback(
        [
            Output("overall-time-line-plot", "figure"),
            Output("boxplot-chart", "figure"),
        ],
        [
            Input("year-dropdown", "value"),
            Input("pilar-dropdown", "value"),
            Input("bank-checklist", "value"),
        ],
    )
    def update_graphs(selected_year, selected_pilar, selected_banks):
        filtered_df = df[
            (df["year"] == selected_year)
            & (df["Predicted_Pilar"] == selected_pilar)
            & (df["Bank Name"].isin(selected_banks))
        ]

        yearly_pilar_line_fig = px.line(
            filtered_df,
            x="date",
            y="Normalized_Sentiment_Score",
            color="Bank Name",
            title=f"Sentiment Score for {selected_year} - {selected_pilar}",
        )
        yearly_pilar_line_fig.update_layout(
            font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
        )
        total_score_line_fig = px.line(
            filtered_df,
            x="date",
            y="Total_Sentiment_Score",
            color="Bank Name",
            title=f"Total Sentiment Score for {selected_year}",
        )
        total_score_line_fig.update_layout(
            font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
        )
        overall_df = (
            df[df["Bank Name"].isin(selected_banks)]
            .groupby(["Bank Name", "date"])
            .agg({"Total_Sentiment_Score": "mean"})
            .reset_index()
        )
        overall_time_line_fig = px.line(
            overall_df,
            x="date",
            y="Total_Sentiment_Score",
            color="Bank Name",
            title="Overall Sentiment Score Over Time",
        )

        overall_time_line_fig.update_layout(
            font=dict(family="Roboto"),
            xaxis=dict(showgrid=True, tickformat="%d-%b", tickangle=-45),
            yaxis=dict(showgrid=True),
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [
                                {
                                    "xaxis": {
                                        "range": [
                                            overall_df["date"].max()
                                            - pd.Timedelta(days=7),
                                            overall_df["date"].max(),
                                        ],
                                        "tickformat": "%d-%b",
                                        "tickangle": -45,
                                    }
                                }
                            ],
                            "label": "1 Semana",
                            "method": "relayout",
                        },
                        {
                            "args": [
                                {
                                    "xaxis": {
                                        "range": [
                                            overall_df["date"].max()
                                            - pd.Timedelta(days=30),
                                            overall_df["date"].max(),
                                        ],
                                        "tickformat": "%d-%b",
                                        "tickangle": -45,
                                    }
                                }
                            ],
                            "label": "1 Mes",
                            "method": "relayout",
                        },
                        {
                            "args": [
                                {
                                    "xaxis": {
                                        "range": [
                                            overall_df["date"].max()
                                            - pd.Timedelta(days=182),
                                            overall_df["date"].max(),
                                        ],
                                        "tickformat": "%b-%Y",
                                        "tickangle": -45,
                                    }
                                }
                            ],
                            "label": "6 Meses",
                            "method": "relayout",
                        },
                        {
                            "args": [
                                {
                                    "xaxis": {
                                        "range": [
                                            overall_df["date"].max()
                                            - pd.Timedelta(days=365),
                                            overall_df["date"].max(),
                                        ],
                                        "tickformat": "%b-%Y",
                                        "tickangle": -45,
                                    }
                                }
                            ],
                            "label": "1 Año",
                            "method": "relayout",
                        },
                        {
                            "args": [
                                {
                                    "xaxis": {
                                        "range": [
                                            overall_df["date"].max()
                                            - pd.Timedelta(days=1095),
                                            overall_df["date"].max(),
                                        ],
                                        "tickformat": "%b-%Y",
                                        "tickangle": -45,
                                    }
                                }
                            ],
                            "label": "3 Años",
                            "method": "relayout",
                        },
                        {
                            "args": [
                                {
                                    "xaxis": {
                                        "range": [
                                            overall_df["date"].min(),
                                            overall_df["date"].max(),
                                        ],
                                        "tickformat": "%b-%Y",
                                        "tickangle": -45,
                                    }
                                }
                            ],
                            "label": "Toda la historia",
                            "method": "relayout",
                        },
                    ],
                    "direction": "left",
                    "showactive": True,
                    "x": 0.5,
                    "xanchor": "center",
                    "y": 1,
                    "yanchor": "top",
                    "type": "buttons",
                }
            ],
        )
        boxplot_fig = px.box(
            filtered_df,
            x="Bank Name",
            y="Normalized_Sentiment_Score",
            color="Bank Name",
            title="Boxplot of Sentiment Scores by Bank",
        )

        return (
            overall_time_line_fig,
            boxplot_fig,
        )


def register_layout_and_callbacks_benchmark(app):
    register_callbacks(app)
