"""
SASB Analysis Layout
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
filtro_sasb = df1["Predicted_SASB"] == "Other"
df_sasb = df1[filtro_sasb]
df_sasb.reset_index(drop=True, inplace=True)
df_grouped = (
    df1.groupby("state").agg({"Normalized_Sentiment_Score": "mean"}).reset_index()
)
df_2 = df_sasb.copy()
df_2 = (
    df_2.groupby(["Bank Name", "Predicted_Pilar", "year", "month_num"])[
        ["Normalized_Sentiment_Score"]
    ]
    .mean()
    .reset_index()
)
df_2["date"] = pd.to_datetime(
    df_2["year"].astype(str) + "-" + df_2["month_num"].map("{:02}".format),
    format="%Y-%m",
)
df_2["Total_Sentiment_Score"] = df_2.groupby(["Bank Name", "date"])[
    "Normalized_Sentiment_Score"
].transform("mean")
df_2.sort_values("date", inplace=True)
sasb_score = df_2[df_2["Bank Name"] == bkn]["Total_Sentiment_Score"].mean()
sasb_gauge_chart, explanation_sasb_gauge_chart = create_gauge_chart(sasb_score)
industry_comments = df_sasb[df_sasb["Industry"] == "Banking"]
industry_comments["Sentiment_Category"] = industry_comments[
    "Normalized_Sentiment_Score"
].apply(categorize_score)
universe_totals = df_sasb["Sentiment_Category"].value_counts(normalize=True) * 100
industry_totals = (
    industry_comments["Sentiment_Category"].value_counts(normalize=True) * 100
)
obj_bank = df_sasb[df_sasb["Bank Name"] == bkn]
total_obj_bank = len(obj_bank)
obj_bank_totals_corrected = (
    obj_bank["Sentiment_Category"].value_counts(normalize=True) * 100
)
percentage_data_corrected = []
for category in ["Poor", "Low", "Medium", "Good", "Excellent"]:
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
    categories=["Poor", "Low", "Medium", "Good", "Excellent"],
    ordered=True,
)
percentage_df_corrected = percentage_df_corrected.sort_values("Category")

fig_hist_sasb = px.bar(
    percentage_df_corrected,
    x="Category",
    y="Percentage",
    color="Type",
    barmode="group",
    text="Percentage",
    height=400,
    category_orders={"Type": category_order},
    color_discrete_map=custom_colors,
)
fig_hist_sasb.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
fig_hist_sasb.update_layout(
    uniformtext_minsize=14,
)

score_by_pillar = (
    df1.groupby("Predicted_SASB")
    .agg(Avg_Score=("Normalized_Sentiment_Score", "mean"))
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

fig_risk_sasb = go.Figure()
fig_risk_sasb.add_shape(
    type="rect",
    x0=0,
    y0=50,
    x1=1,
    y1=100,
    fillcolor="lightgreen",
    opacity=0.5,
    line_width=0,
)
fig_risk_sasb.add_shape(
    type="rect",
    x0=0,
    y0=0,
    x1=1,
    y1=50,
    fillcolor="lightcoral",
    opacity=0.5,
    line_width=0,
)
for sentiment in df_sasb["Sentiment_gen"].unique():
    filtered_df_1 = df_sasb[df_sasb["Sentiment_gen"] == sentiment]
    fig_risk_sasb.add_trace(
        go.Scatter(
            x=filtered_df_1["Total_Count"],
            y=filtered_df_1["Normalized_Sentiment_Score"],
            mode="markers",
            name=sentiment,
            marker=dict(size=6, line=dict(width=1)),
        )
    )
fig_risk_sasb.update_layout(
    title="Sentiment vs Exposure and Management",
    xaxis_title="Exposure (Total_Count)",
    yaxis_title="Sentiment (Normalized_Sentiment_Score)",
    showlegend=True,
    annotations=[
        dict(
            x=0.1,
            y=0.95,
            text="Strong",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black"),
        ),
        dict(
            x=0.1,
            y=0.05,
            text="Weak",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black"),
        ),
        dict(
            x=0.05,
            y=0.5,
            text="Sentiment",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black"),
            textangle=-90,
        ),
        dict(
            x=0.5,
            y=0.02,
            text="Low",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black"),
        ),
        dict(
            x=0.95,
            y=0.02,
            text="High",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black"),
        ),
        dict(
            x=0.95,
            y=0.95,
            text="Negligible Risk",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black"),
        ),
        dict(
            x=0.95,
            y=0.05,
            text="Severe Risk",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black"),
        ),
    ],
)
SASB_ANALYSIS_LAYOUT = html.Div(
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
                                            id="gauge-chart", figure=sasb_gauge_chart
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
                                            children=[explanation_sasb_gauge_chart],
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
                                        dcc.Graph(id="histogram", figure=fig_hist_sasb)
                                    ],
                                ),
                                html.Div(
                                    className="col-6",
                                    children=[
                                        create_result_table(df_sasb),
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
                            children=[
                                html.H3(children=["Analisis Geografico Pilar SASB"])
                            ],
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-6",
                                    style={
                                        "display": "flex",
                                        "flexDirection": "column",
                                        "alignItems": "stretch",
                                    },
                                    children=dcc.Graph(id="sasb-map"),
                                ),
                                html.Div(
                                    className="col-6",
                                    style={
                                        "display": "flex",
                                        "flexDirection": "column",
                                        "alignItems": "stretch",
                                    },
                                    children=html.Div(id="sasb-table"),
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
                            children=[
                                html.H3(children=["Analisis De Impacto y Riesgo SASB"])
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
                                    children=[
                                        dcc.Graph(id="risk-fig", figure=fig_risk_sasb)
                                    ],
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
        [Output("sasb-map", "figure"), Output("sasb-table", "children")],
        [Input("sasb-map", "clickData")],
    )
    def update_sasb_map(click_data):
        filtered_df = df_sasb.copy()
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


def register_layout_and_callbacks_sasb(app):
    register_callbacks(app)
