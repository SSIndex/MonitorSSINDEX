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
    categorize_score_to_bg_class_name,
    categorize_score_to_text_class_name,
)
from DashMonitor.app.data.analyzers.map_analyzer import MapAnalyzer

# Import mock data
from DashMonitor.app.views.layouts.mock_data_geographic_analysis import *
from DashMonitor.app.views.configs import (
    main_df_provider,
    COMPANY_NAME,
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
filtro_general = (df["Pilar"] == "Other") & (df["Predicted_SASB"] == "Other")
df = df[filtro_general].reset_index(drop=True)

analyzer = MapAnalyzer(main_df_provider, None)
reviews_data = analyzer.get_all_reviews_by_company(COMPANY_NAME)
data_analyzed_df = analyzer.execute()

nested_data = [
    [
        html.P(row['review']),
        html.P(
            className=f"{categorize_score_to_text_class_name(row['sentiment_score'])}",
            children=f"{row['sentiment_score']}%",
        ),
        html.P(
            className=f"{categorize_score_to_text_class_name(row['sentiment_score'])}",
            children=f"{categorize_score(row['sentiment_score'])}",
        ),
        html.P(row['state']),
        html.P(row['ds']),
        html.P(row['data_source']),
    ]
    for _, row in reviews_data.iterrows()
]

empty_circle_style = {
    "width": "50px",
    "height": "50px",
    "border-radius": "50%",
    "display": "inline-block",
}

html_data = [
    {
        "data": [
            html.Div(
                className=f"{categorize_score_to_bg_class_name(row['sentiment_score'])}",
                style=empty_circle_style,
                children=html.P("\u200B"),
            ),
            html.P(row['state']),
            html.Div(
                className=f"{categorize_score_to_bg_class_name(row['sentiment_score'])} w-100 h-100 border rounded",
                children=html.B(
                    className='text-white', children=f"{round(row['sentiment_score'])}"
                ),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 border rounded",
                children=html.B(className='text-white', children="100th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    }
    for _, row in data_analyzed_df.iterrows()
]

GEOGRAPHIC_ANALYSIS_LAYOUT = html.Div(
    className="container",
    children=[
        # Date Picker Secion
        html.Section(
            className='section pt-3 d-flex justify-content-end',
            children=[cpt.DatePicker().render()],
        ),
        html.Section(
            className="section pt-5",
            children=[
                html.Div(
                    children=[
                        html.H4(
                            className="text-primary", children=['Geographical Analysis']
                        ),
                        html.P(
                            className='text-ssindex-graph-grey',
                            children=['Stakeholders feedback classified by territory'],
                        ),
                        cpt.Table(
                            headers=headers,
                            data=html_data,
                            class_name_headers=class_name_headers,
                        ).render(),
                    ]
                )
            ],
        ),
    ],
)


# def register_callbacks(app):
#     @app.callback(
#         [Output("general-map", "figure"), Output("general-table", "children")],
#         [Input("general-map", "clickData")],
#     )
#     def update_general_map(click_data):
#         filtered_df = df.copy()
#         filtered_df = filtered_df[filtered_df["Bank Name"] == bkn]
#         df_grouped = (
#             filtered_df.groupby("state").agg({"Sentiment_Score": "mean"}).reset_index()
#         )
#         df_grouped["color"] = df_grouped["Sentiment_Score"].apply(
#             lambda x: "blue" if x > 0 else "red"
#         )

#         fig = go.Figure(
#             data=go.Choropleth(
#                 locations=df_grouped["state"],
#                 z=df_grouped["Sentiment_Score"],
#                 locationmode="USA-states",
#                 colorscale="Blues",
#                 marker_line_color="white",
#             )
#         )
#         fig.update_layout(
#             title_text=f"Average Sentiment Score by State for {bkn}",
#             geo_scope="usa",
#         )
#         reviews_table = html.Table()
#         if click_data:
#             state = click_data["points"][0]["location"]
#             reviews = filtered_df[filtered_df["state"] == state][
#                 ["Review", "Sentiment_Score", "Bank Name"]
#             ].head(5)
#             reviews_table = html.Table(
#                 [
#                     html.Thead(
#                         html.Tr(
#                             [
#                                 html.Th(
#                                     col,
#                                     style={
#                                         "padding": "10px",
#                                         "border": "1px solid black",
#                                     },
#                                 )
#                                 for col in reviews.columns
#                             ]
#                         )
#                     ),
#                     html.Tbody(
#                         [
#                             html.Tr(
#                                 [
#                                     html.Td(
#                                         reviews.iloc[i][col],
#                                         style={
#                                             "padding": "10px",
#                                             "border": "1px solid black",
#                                         },
#                                     )
#                                     for col in reviews.columns
#                                 ]
#                             )
#                             for i in range(len(reviews))
#                         ]
#                     ),
#                 ],
#                 style={
#                     "width": "100%",
#                     "borderCollapse": "collapse",
#                     "marginTop": "20px",
#                 },
#             )
#         return fig, reviews_table


def register_layout_and_callbacks_map(app):
    # register_callbacks(app)
    pass
