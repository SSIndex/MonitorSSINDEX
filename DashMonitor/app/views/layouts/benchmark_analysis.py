"""
BENCHMARK Analysis Layout
"""

# std imports
from datetime import date
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, Input, Output, State


# 3rd party imports
from dash import html

# local imports
from DashMonitor.app.data.analyzers import TimeTrendAnalyzer
from DashMonitor.app.handlers.date_utils import DateUtils
from DashMonitor.app.handlers.function_utils import (
    categorize_score,
    categorize_score_to_text_class_name,
)

from DashMonitor.app.views import components as cpt

# Import mock data
from DashMonitor.app.views.components.date_picker.callbacks import (
    register_datepicker_callbacks,
)
from DashMonitor.app.views.components.date_picker.date_picker import DatePicker
from DashMonitor.app.views.components.utils.button import ButtonUtils
from DashMonitor.app.views.layouts.mock_data_sasb_analysis import *
from DashMonitor.app.views.configs import (
    main_df_provider,
    COMPANY_NAME,
)


analyzer = TimeTrendAnalyzer(main_df_provider, None)

reviews_data = analyzer.get_all_reviews_by_company(COMPANY_NAME)

data_frame = analyzer.execute()

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

from dash import html

data = [
    {"data": nested_data[0]},
    {"data": nested_data[1]},
    {"data": nested_data[2]},
]

df = data_frame
# Your imports and code...
html_data = [
    {
        "data": [
            html.P(row["review"]),
            html.P(
                className=f"{categorize_score_to_text_class_name(row['sentiment_score'])}",
                children=f"{row['sentiment_score']}%",
            ),
            html.P(
                className=f"{categorize_score_to_text_class_name(row['sentiment_score'])}",
                children=f"{categorize_score(row['sentiment_score'])}",
            ),
            html.P(row['pilar']),
            html.P(row['dimension_sasb']),
            html.P(row['state']),
            html.P(row['state']),
            html.P(row['ds']),
            html.P(row['data_source']),
        ]
    }
    for _, row in reviews_data.iterrows()
]

BENCHMARK_ANALYSIS_LAYOUT = html.Div(
    className="container",
    children=[
        # Date Picker Section
        html.Section(
            className='section pt-3 d-flex justify-content-end',
            children=[cpt.DatePicker(disabled=False).render()],
        ),
        # Time trend - Local Industry Analysis Section
        html.Section(
            className="section pt-3",
            children=[
                html.H5(
                    className='text-primary',
                    children=["Time trend - Local Industry Analysis"],
                ),
                html.P(
                    children=[
                        "Stakeholders feedback classified by company, operating locally, and by time"
                    ]
                ),
                html.Div(
                    className="bg-white rounded rounded-4 p-3 shadow-sm",
                    children=[dcc.Graph(id="overall-time-line-plot")],
                ),
            ],
        ),
        # Table Section
        html.Section(
            className="section mt-4 p-3 rounded rounded-4 bg-ssindex-nested-table-background shadow-sm",
            children=[
                cpt.Table(
                    headers=nested_headers,
                    data=html_data,
                    class_name_div="table-ssindex-nested-table-background text-center rounded-3",
                    class_name_table="table table-borderless table-responsive table-ssindex-nested-table-background rounded rounded-3",
                    class_name_headers="text-center table-white align-middle",
                ).render()
            ],
        ),
        # Box plot - Local Industry Analysis Section
        html.Section(
            className="section pt-3",
            children=[
                html.H5(
                    className='text-primary',
                    children=["Box plot - Local Industry Analysis"],
                ),
                html.P(
                    children=[
                        "Stakeholders feedback classified by company, operating locally, and by time"
                    ]
                ),
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="bg-white rounded rounded-4 p-3 shadow-sm",
                            children=[dcc.Graph(id="boxplot-chart")],
                        ),
                    ],
                ),
            ],
        ),
        html.Section(
            className="section bg-white pt-3 mt-4",
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
                                                    "predicted_pilar"
                                                ].unique()
                                            ],
                                            value=df["predicted_pilar"].unique()[0],
                                            clearable=False,
                                        ),
                                        dcc.Dropdown(
                                            id="bank-dropdown",
                                            options=[
                                                {"label": bank, "value": bank}
                                                for bank in df["bank_name"].unique()
                                            ],
                                            value=df["bank_name"].unique()[0],
                                            clearable=False,
                                        ),
                                        dcc.Checklist(
                                            id="bank-checklist",
                                            options=[
                                                {"label": name, "value": name}
                                                for name in df["bank_name"].unique()
                                            ],
                                            value=["Boeing"],
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
                    ],
                ),
            ],
        ),
    ],
)


def register_callbacks(app):
    @app.callback(
        [
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
            & (df["predicted_pilar"] == selected_pilar)
            & (df["bank_name"].isin(selected_banks))
        ]

        boxplot_fig = px.box(
            filtered_df,
            x="bank_name",
            y="sentiment_score",
            color="bank_name",
        )

        boxplot_fig.update_layout(
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

        return (boxplot_fig,)

    @app.callback(
        Output("overall-time-line-plot", "figure"),
        Input('submit-btn', 'n_clicks'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        [State(btn_id, 'className') for btn_id in DatePicker.BUTTON_IDS],
    )
    def update_line_graph(n_clicks, start_date, end_date, *button_classes):
        """
        Updates the line graph based on the selected date range or button.
        If a date range is selected manually, it uses that range;
        otherwise, it uses predefined date range buttons.
        """

        # Convert dates if manually selected
        if start_date and end_date:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
        else:
            # If a predefined button is selected, determine the corresponding date range
            selected_index = ButtonUtils.selected_button_index(button_classes)
            end_date = pd.to_datetime(date.today())
            start_date = pd.to_datetime(DateUtils().calculate_start_date_on_index(selected_index))

        # Aggregate sentiment scores by bank name and date
        overall_df = (
            df.groupby(["bank_name", "date"])
            .agg(total_sentiment_score=("total_sentiment_score", "mean"))
            .reset_index()
        )

        # Filter the data according to the selected date range
        overall_df = overall_df[overall_df["date"].between(start_date, end_date)]

        # Create the line plot
        overall_time_line_fig = px.line(
            overall_df,
            x="date",
            y="total_sentiment_score",
            color="bank_name",
        )

        # Update layout properties for clarity and aesthetics
        overall_time_line_fig.update_layout(
            font=dict(family="Roboto"),
            xaxis=dict(showgrid=True, tickformat="%d-%b", tickangle=-45),
            yaxis=dict(showgrid=True),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="center",
                x=0.5,
            ),
            yaxis_title="",
            xaxis_title="",
            legend_title="",
        )

        # Set x-axis date format
        overall_time_line_fig.update_xaxes(tickformat="%d %b %Y")

        return overall_time_line_fig


def register_layout_and_callbacks_benchmark(app):
    register_callbacks(app)
    register_datepicker_callbacks(app)
