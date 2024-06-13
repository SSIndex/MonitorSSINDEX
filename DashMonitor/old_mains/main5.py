import dash
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def sentiment_color(score):
    if score <= 50:
        return "red"
    elif score <= 75:
        return "yellow"
    else:
        return "green"


def create_gauge_chart(score):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode="gauge",
            value=score,
            domain={'x': [0.1, 1], 'y': [0.2, 0.8]},
            title={'text': "Score", 'font': {'size': 24}, 'align': 'center'},
            gauge={
                'shape': "bullet",
                'axis': {
                    'range': [0, 100],
                    'tickmode': 'array',
                    'tickvals': [],
                    'ticktext': [],
                    'tickwidth': 2,
                    'tickcolor': 'darkblue',
                },
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 20], 'color': "#F44336"},  # Red for Very Low
                    {'range': [21, 40], 'color': "#FF9800"},  # Orange for Low
                    {'range': [41, 60], 'color': "#FFEB3B"},  # Yellow for Medium
                    {'range': [61, 80], 'color': "#2196F3"},  # Blue for High
                    {'range': [81, 100], 'color': "#4CAF50"},  # Green for Very High
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.75,
                    'value': score,
                },
            },
        )
    )

    fig.update_layout(
        height=180,
        margin={'t': 40, 'b': 20, 'l': 40, 'r': 20},
        annotations=[
            dict(
                x=0.14,
                y=0,
                text="Very Low",
                showarrow=False,
                font=dict(size=10),
                xanchor='center',
            ),
            dict(
                x=0.33,
                y=0,
                text="Low",
                showarrow=False,
                font=dict(size=10),
                xanchor='center',
            ),
            dict(
                x=0.52,
                y=0,
                text="Medium",
                showarrow=False,
                font=dict(size=10),
                xanchor='center',
            ),
            dict(
                x=0.71,
                y=0,
                text="High",
                showarrow=False,
                font=dict(size=10),
                xanchor='center',
            ),
            dict(
                x=0.9,
                y=0,
                text="Very High",
                showarrow=False,
                font=dict(size=10),
                xanchor='center',
            ),
        ],
        title={
            'text': f"{int(score)} /100",
            'y': 0.9,
            'x': 0.55,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 44},
        },
    )

    if score <= 20:
        category = "Very Low"
        explanation = "This company has a very low sentiment score. Approximately 80% of the comments are negative, and only 20% are positive."
    elif score <= 40:
        category = "Low"
        explanation = "This company has a low sentiment score. Around 60% of the comments are negative, and 40% are positive."
    elif score <= 60:
        category = "Medium"
        explanation = "This company has a medium sentiment score. About 50% of the comments are positive, and 50% are negative."
    elif score <= 80:
        category = "High"
        explanation = "This company has a high sentiment score. Approximately 60% of the comments are positive, and 40% are negative."
    else:
        category = "Very High"
        explanation = "This company has a very high sentiment score. Around 80% of the comments are positive, and only 20% are negative."

    explanation_string = f"Category: {category}\n\n" f"{explanation}\n\n"

    return fig, explanation_string


bkn = "Webster Bank"
# df = pd.read_csv("data/processed_webster.csv")
df = pd.read_csv("data/Sentiment_Data_with_Normalized_Score.csv")
df["Nuevo_Sentiment_Score"] = df["Normalized_Sentiment_Score"]
# df["Nuevo_Sentiment_Score"] = df["Smoothed_Sentiment_Score"]
df["ds"] = pd.to_datetime(df["ds"])
df1 = df.copy()

month_map = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}

df["month_num"] = df["month"].map(month_map)
df = (
    df.groupby(["Bank Name", "Predicted_Pilar", "year", "month_num"])[
        ["Nuevo_Sentiment_Score"]
    ]
    .mean()
    .reset_index()
)
df["date"] = pd.to_datetime(
    df["year"].astype(str) + "-" + df["month_num"].map("{:02}".format), format="%Y-%m"
)
df["Total_Sentiment_Score"] = df.groupby(["Bank Name", "date"])[
    "Nuevo_Sentiment_Score"
].transform("mean")
df.sort_values("date", inplace=True)

state_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

df1["state"] = df1["state"].map(state_abbrev)
df_grouped = (
    df1.groupby("state").agg({"Normalized_Sentiment_Score": "mean"}).reset_index()
)
df_grouped["color"] = df_grouped["Normalized_Sentiment_Score"].apply(sentiment_color)
colorscale = [[0, "red"], [0.5, "yellow"], [1, "green"]]

external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.index_string = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor SSINDEX</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    <link rel="icon" type="image/x-icon" href="monitorImages/IsotipoNegativo.svg">
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
"""

aux = df1[df1["Bank Name"] == bkn]

source_data = aux.groupby('data_source').size().reset_index(name='counts')
fig_pie = px.pie(
    source_data,
    values='counts',
    names='data_source',
    title=f'Data Source Distribution for {bkn}',
)
category_order = ['Very Low', 'Low', 'Medium', 'High', 'Very High']

hist_data = aux.groupby(['New_Sentiment_Score']).size().reset_index(name='counts')
hist_data['New_Sentiment_Score'] = pd.Categorical(
    hist_data['New_Sentiment_Score'], categories=category_order, ordered=True
)

hist_data = hist_data.sort_values('New_Sentiment_Score')
fig_hist = go.Figure()
fig_hist.add_trace(
    go.Bar(
        x=hist_data['New_Sentiment_Score'],
        y=hist_data['counts'],
        text=hist_data['counts'],
        textposition='auto',
        name='Reviews',
        marker_color='blue',
    )
)
fig_hist.update_layout(title_text=f'Sentiment Score Distribution for {bkn}')
initial_score = df[df["Bank Name"] == bkn]["Total_Sentiment_Score"].values[-1]
initial_gauge_chart, explanation_gauge_chart = create_gauge_chart(initial_score)

# Layout of the Dash app
app.layout = html.Div(
    [
        html.Header(
            className="bg-dark text-white",
            children=[
                dbc.Container(
                    [
                        dbc.Navbar(
                            dbc.Container(
                                [
                                    html.A(
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.NavbarBrand(
                                                        "Monitor SSINDEX",
                                                        className="ms-2",
                                                    )
                                                ),
                                            ],
                                            align="center",
                                            className="g-0",
                                        ),
                                        href="/",
                                        style={"textDecoration": "none"},
                                    ),
                                    dbc.NavbarToggler(id="navbar-toggler"),
                                    dbc.Collapse(
                                        dbc.Nav(
                                            [
                                                dbc.NavItem(
                                                    dbc.NavLink(
                                                        "Home", active=True, href="#"
                                                    )
                                                ),
                                                dbc.NavItem(
                                                    dbc.NavLink("Features", href="#")
                                                ),
                                                dbc.NavItem(
                                                    dbc.NavLink("Pricing", href="#")
                                                ),
                                                dbc.NavItem(
                                                    dbc.NavLink("About", href="#")
                                                ),
                                            ],
                                            className="ms-auto",
                                            navbar=True,
                                        ),
                                        id="navbar-collapse",
                                        navbar=True,
                                    ),
                                ]
                            ),
                            color="dark",
                            dark=True,
                        )
                    ]
                )
            ],
        ),
        html.Main(
            className="container container-fluid pt-2",
            children=[
                dbc.Tabs(
                    [
                        dbc.Tab(label="General", tab_id="general"),
                        dbc.Tab(label="SASB", tab_id="sasb"),
                        dbc.Tab(label="SSINDEX", tab_id="ssindex"),
                        dbc.Tab(label="Industry Comparisson", tab_id="bench"),
                    ],
                    id="tabs",
                    active_tab="general",
                ),
                html.Div(id="tab-content"),
            ],
        ),
        html.Footer(
            className="footer bg-dark text-white py-3",
            children=[dbc.Container(html.P("© 2024 SSINDEX", className="mb-0"))],
        ),
    ]
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_content(tab):
    if tab == "general":
        return html.Div(
            [
                html.Div(
                    className="section bg-light",
                    children=[
                        dbc.Container(
                            className="border-bottom border-dark",
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.P("2024-05-16", className="text-end"),
                                            width=12,
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Row(html.H4(bkn)),
                                                dbc.Row(
                                                    html.P("Bank | EEUU | Market Name")
                                                ),
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                id="gauge-chart",
                                                figure=initial_gauge_chart,
                                            ),
                                            width=6,
                                        ),
                                    ]
                                ),
                            ],
                        )
                    ],
                ),
                html.Div(
                    className="section bg-white",
                    children=[
                        dbc.Container(
                            className="border-bottom border-dark",
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Graph(
                                                    id='histogram', figure=fig_hist
                                                )
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(html.P(explanation_gauge_chart)),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [dcc.Graph(id='pie-chart', figure=fig_pie)],
                                            width=6,
                                        ),
                                        dbc.Col(
                                            [
                                                html.Img(
                                                    src="/assets/rankComparisson.png",
                                                    alt="Rank Comparisson",
                                                ),
                                                html.P(
                                                    "Tabla Posición y Percentil de Compañía y Universo"
                                                ),
                                            ],
                                            width=6,
                                        ),
                                    ]
                                ),
                            ],
                        )
                    ],
                ),
            ]
        )
    elif tab == "bench":
        return html.Div(
            [
                html.Div(
                    className="section bg-white",
                    children=[
                        dbc.Container(
                            className="border-bottom border-dark",
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [dcc.Graph(id='overall-time-line-plot')],
                                            width=8,
                                        ),
                                        dbc.Col(
                                            [
                                                html.Img(
                                                    src="assets/ssindex.png",
                                                    style={
                                                        "height": "60px",
                                                        "margin": "10px",
                                                    },
                                                ),
                                                html.Div(
                                                    id="selected-bank",
                                                    style={
                                                        "font-size": "20px",
                                                        "font-weight": "bold",
                                                        "margin": "10px",
                                                    },
                                                ),
                                                html.Div(
                                                    [
                                                        dcc.Dropdown(
                                                            id="year-dropdown",
                                                            options=[
                                                                {
                                                                    "label": str(year),
                                                                    "value": year,
                                                                }
                                                                for year in df[
                                                                    "year"
                                                                ].unique()
                                                            ],
                                                            value=df["year"].max(),
                                                            clearable=False,
                                                        ),
                                                        dcc.Dropdown(
                                                            id="pilar-dropdown",
                                                            options=[
                                                                {
                                                                    "label": pilar,
                                                                    "value": pilar,
                                                                }
                                                                for pilar in df[
                                                                    "Predicted_Pilar"
                                                                ].unique()
                                                            ],
                                                            value=df[
                                                                "Predicted_Pilar"
                                                            ].unique()[0],
                                                            clearable=False,
                                                        ),
                                                        dcc.Dropdown(
                                                            id="bank-dropdown",
                                                            options=[
                                                                {
                                                                    "label": bank,
                                                                    "value": bank,
                                                                }
                                                                for bank in df[
                                                                    "Bank Name"
                                                                ].unique()
                                                            ],
                                                            value=df[
                                                                "Bank Name"
                                                            ].unique()[2],
                                                            clearable=False,
                                                        ),
                                                        dcc.Checklist(
                                                            id="bank-checklist",
                                                            options=[
                                                                {
                                                                    "label": name,
                                                                    "value": name,
                                                                }
                                                                for name in df[
                                                                    "Bank Name"
                                                                ].unique()
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
                                            width=4,
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [dcc.Graph(id='boxplot-chart')],
                                            width=4,
                                        ),
                                        dbc.Col(
                                            [
                                                html.Img(
                                                    src="/assets/rankComparisson.png",
                                                    alt="Rank Comparisson",
                                                ),
                                                html.P(
                                                    "Tabla Posición y Percentil de Compañía y Universo"
                                                ),
                                            ],
                                            width=6,
                                        ),
                                    ]
                                ),
                            ],
                        )
                    ],
                ),
            ]
        )

    # Manejar otras pestañas de manera similar
    return html.Div("Content for {}".format(tab))


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
        y="Nuevo_Sentiment_Score",
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
        xaxis=dict(showgrid=True, tickformat='%d-%b', tickangle=-45),
        yaxis=dict(showgrid=True),
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            {
                                "xaxis": {
                                    "range": [
                                        overall_df['date'].max() - pd.Timedelta(days=7),
                                        overall_df['date'].max(),
                                    ],
                                    "tickformat": '%d-%b',
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
                                        overall_df['date'].max()
                                        - pd.Timedelta(days=30),
                                        overall_df['date'].max(),
                                    ],
                                    "tickformat": '%d-%b',
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
                                        overall_df['date'].max()
                                        - pd.Timedelta(days=182),
                                        overall_df['date'].max(),
                                    ],
                                    "tickformat": '%b-%Y',
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
                                        overall_df['date'].max()
                                        - pd.Timedelta(days=365),
                                        overall_df['date'].max(),
                                    ],
                                    "tickformat": '%b-%Y',
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
                                        overall_df['date'].max()
                                        - pd.Timedelta(days=1095),
                                        overall_df['date'].max(),
                                    ],
                                    "tickformat": '%b-%Y',
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
                                        overall_df['date'].min(),
                                        overall_df['date'].max(),
                                    ],
                                    "tickformat": '%b-%Y',
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

    start_date = "2016-04-30"
    df_filtered = df1[df1["ds"] >= start_date]
    df_grouped_1 = (
        df_filtered.groupby(["Bank Name", pd.Grouper(key="ds", freq="ME")])[
            "Nuevo_Sentiment_Score"
        ]
        .mean()
        .reset_index()
    )
    df_pivot = df_grouped_1.pivot(
        index="Bank Name", columns="ds", values="Nuevo_Sentiment_Score"
    )
    heatmap_fig = go.Figure(
        data=go.Heatmap(
            z=df_pivot.values,
            x=df_pivot.columns,
            y=df_pivot.index,
            colorscale="Viridis",
            colorbar=dict(title="Average Sentiment Score"),
        )
    )
    heatmap_fig.update_layout(
        title="Heatmap of Average Sentiment Scores", xaxis_nticks=36
    )

    filtered_df_2 = df[(df["Bank Name"].isin(selected_banks))]
    filtered_df_2 = (
        filtered_df_2.groupby(["Bank Name", "year"])
        .agg({"Nuevo_Sentiment_Score": "mean", "Total_Sentiment_Score": "mean"})
        .reset_index()
    )

    bubble_fig = px.scatter(
        filtered_df_2,
        x="year",
        y="Nuevo_Sentiment_Score",
        size="Total_Sentiment_Score",
        color="Bank Name",
        title="Bubble Chart",
    )
    bubble_fig.update_layout(
        font=dict(family="Roboto"),
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
    )

    boxplot_fig = px.box(
        filtered_df,
        x="Bank Name",
        y="Nuevo_Sentiment_Score",
        color="Bank Name",
        title="Boxplot of Sentiment Scores by Bank",
    )
    violin_fig = px.violin(
        filtered_df,
        x="Bank Name",
        y="Nuevo_Sentiment_Score",
        color="Bank Name",
        title="Violin Plot of Sentiment Scores by Bank",
    )
    selected_bank_text = f"Currently Evaluating: {', '.join(selected_banks)}"

    return (
        overall_time_line_fig,
        boxplot_fig,
    )


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8052)
