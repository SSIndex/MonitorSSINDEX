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
from DashMonitor.app.views import components as cpt

category_order = ["Universe", "Industry", "Company"]
custom_colors = {
    "Universe": "#1f77b4",  # Blue
    "Industry": "#2ca02c",  # Green
    "Company": "#ff7f0e",  # Orange
}

bkn = "Webster Bank"

df = pd.read_csv("/app/DashMonitor/data/data_procesa_inferencia_webster_SASB.csv")
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

# Example data for custom components
company_name = bkn  # 'Webster Bank'
industry = 'Bank'
country = 'EEUU'
company_image = 'https://wallpaperaccess.com/full/1642272.jpg'
overview = 'Medium'
overview_text = 'This company holds a medium sentiment score. Feedback is evenly split, with 50% of comments being positive and 50% negative. This indicates a balanced perception among respondents.'
overview_graph = html.Div(
    className="col",
    children=[dcc.Graph(id="gauge-chart", figure=sasb_gauge_chart)],
)
headers = [
    "Dimension ESG",
    html.P(className="align-center text-ssindex-graph-grey mb-0", children="No Data"),
    html.P(className="align-center text-ssindex-poor mb-0", children="Poor"),
    html.P(className="align-center text-ssindex-low mb-0", children="Low"),
    html.P(className="align-center text-ssindex-average mb-0", children="Average"),
    html.P(className="align-center text-ssindex-good mb-0", children="Good"),
    html.P(className="align-center text-ssindex-excellent mb-0", children="Excellent"),
    "Score",
    "Percentil",
]
nested_headers = ["Review", "Sentiment Score", "Category", "ESG Pilar", "Dimension", "Territory or State", "City", "Date", "Source"]
nested_data = [[html.P(children="I called and called an no one answered the phone"), html.P("8%"), html.P(className="text-ssindex-poor", children="Poor"), html.P("Social External"), html.P("Complaints"), html.P("New York"), html.P("New York"), html.P("12/08/23"), html.P("Google")],
               [html.P("I called and called an no one answered the phone"), html.P("12%"), html.P(className="text-ssindex-poor", children="Poor"), html.P("Social External"), html.P("Complaints"), html.P("California"), html.P("Los Angeles"), html.P("05/07/24"), html.P("Instagram")],
                [html.P("I had a problem with one of the products, called, no one answered, then sent an email and the got back to me in two days. Fortunately the problem was solved"), html.P("54%"), html.P(className='text-ssindex-average',children="Average"), html.P("Social External"), html.P("Complaints"), html.P("Texas"), html.P("Houston"), html.P("24/04/24"), html.P("Facebook")],
               ]
data = [
    {
        "data": [
            html.P(className='text-primary align-middle mb-0', children="Environment"),
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
                className="bg-ssindex-average border border-dark border-4 w-100 h-100", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="45%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(
                className='text-primary align-middle mb-0', children="Social Capital"
            ),
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
                className="bg-ssindex-poor w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="15%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.P(
                className='text-primary align-middle mb-0', children="Human Capital"
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 border border-dark border-4", children="\u200B"
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
                className="bg-ssindex-low w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="30%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(
                className='text-primary align-middle mb-0',
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
                className="bg-ssindex-good w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="65%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(
                className='text-primary align-middle mb-0',
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
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className='text-primary align-middle mb-0', children="Others"),
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
                className="bg-ssindex-no-data w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
]
footer_data = [
    html.P(className='text-primary align-middle mb-0', children="Total Score"),
    "",
    "",
    "",
    "",
    "",
    "",
    html.Div(
        className="bg-ssindex-average w-100 h-100 text-center border rounded",
        children=html.B(className='text-white', children="45%"),
    ),
    html.Div(
        className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
        children=html.B(className='text-white', children="20th"),
    ),
]

class_name_headers = 'bg-ssindex-table-header-gray'

SASB_ANALYSIS_LAYOUT = html.Div(
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
                    overview_graph,
                ).render(),
            ],
        ),
        html.Section(
            className="section pt-5",
            children=[
                html.Div(
                    children=[
                        html.H4(
                            className="text-primary", children=['SASB Impact Analysis']
                        ),
                        html.P(
                            className='text-ssindex-graph-grey',
                            children=[
                                'Stakeholders evaluate how the company is performing according to the Sustainability Accounting Standards Board (SASB)smethodology'
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
    ],
)


def register_callbacks(app):
    pass
    # @app.callback(
    #     [Output("sasb-map", "figure"), Output("sasb-table", "children")],
    #     [Input("sasb-map", "clickData")],
    # )
    # def update_sasb_map(click_data):
    #     filtered_df = df_sasb.copy()
    #     filtered_df = filtered_df[filtered_df["Bank Name"] == bkn]
    #     df_grouped = (
    #         filtered_df.groupby("state").agg({"Sentiment_Score": "mean"}).reset_index()
    #     )
    #     df_grouped["color"] = df_grouped["Sentiment_Score"].apply(
    #         lambda x: "blue" if x > 0 else "red"
    #     )

    #     fig = go.Figure(
    #         data=go.Choropleth(
    #             locations=df_grouped["state"],
    #             z=df_grouped["Sentiment_Score"],
    #             locationmode="USA-states",
    #             colorscale="Blues",
    #             marker_line_color="white",
    #         )
    #     )
    #     fig.update_layout(
    #         title_text=f"Average Sentiment Score by State for {bkn}",
    #         geo_scope="usa",
    #     )
    #     reviews_table = html.Table()
    #     if click_data:
    #         state = click_data["points"][0]["location"]
    #         reviews = filtered_df[filtered_df["state"] == state][
    #             ["Review", "Sentiment_Score", "Bank Name"]
    #         ].head(5)
    #         reviews_table = html.Table(
    #             [
    #                 html.Thead(
    #                     html.Tr(
    #                         [
    #                             html.Th(
    #                                 col,
    #                                 style={
    #                                     "padding": "10px",
    #                                     "border": "1px solid black",
    #                                 },
    #                             )
    #                             for col in reviews.columns
    #                         ]
    #                     )
    #                 ),
    #                 html.Tbody(
    #                     [
    #                         html.Tr(
    #                             [
    #                                 html.Td(
    #                                     reviews.iloc[i][col],
    #                                     style={
    #                                         "padding": "10px",
    #                                         "border": "1px solid black",
    #                                     },
    #                                 )
    #                                 for col in reviews.columns
    #                             ]
    #                         )
    #                         for i in range(len(reviews))
    #                     ]
    #                 ),
    #             ],
    #             style={
    #                 "width": "100%",
    #                 "borderCollapse": "collapse",
    #                 "marginTop": "20px",
    #             },
    #         )
    #     return fig, reviews_table


def register_layout_and_callbacks_sasb(app):
    register_callbacks(app)
