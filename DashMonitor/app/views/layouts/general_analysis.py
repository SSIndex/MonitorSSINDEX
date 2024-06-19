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
category_order = ["Universe", "Industry", "Company"]
custom_colors = {
    "Universe": "#1f77b4",  # Blue
    "Industry": "#2ca02c",  # Green
    "Company": "#ff7f0e",  # Orange
}


def categorize_score(score):
    if score <= 20:
        return "Poor"
    elif score <= 40:
        return "Low"
    elif score <= 60:
        return "Medium"
    elif score <= 80:
        return "Good"
    else:
        return "Excellent"


def create_result_table(data):
    """
    Creates a result table based on the given data.

    Args:
        data (pandas.DataFrame): The input data containing bank names and sentiment scores.

    Returns:
        dash_table.DataTable: The result table as a Dash DataTable object.
    """
    # Calcular el total de comentarios y el promedio del puntaje para cada compañía
    company_stats = (
        data.groupby("Bank Name")
        .agg(
            Total_Comments=("Normalized_Sentiment_Score", "size"),
            Avg_Score=("Normalized_Sentiment_Score", "mean"),
        )
        .reset_index()
    )

    # Ordenar por el puntaje promedio
    company_stats = company_stats.sort_values(
        by="Avg_Score", ascending=False
    ).reset_index(drop=True)

    # Calcular la posición de la compañía en el universo y la industria
    company_stats["Position_Universe"] = company_stats.index + 1
    company_stats["Position_Industry"] = (
        company_stats.index + 1
    )  # Solo hay una industria en este caso

    # Calcular el percentil de la compañía
    company_stats["Percentile_Universe"] = (
        company_stats["Avg_Score"].rank(pct=True) * 100
    )
    company_stats["Percentile_Industry"] = (
        company_stats["Avg_Score"].rank(pct=True) * 100
    )  # Solo hay una industria en este caso

    # Filtrar los datos para la tabla final
    webster_stats = company_stats[company_stats["Bank Name"] == "Webster Bank"]

    # Crear la tabla de resultados
    result_table = pd.DataFrame(
        {
            "Type": [
                "Global Universe",
                "Technology Hardware (Industry)",
                "Communications Equipment (Subindustry)",
            ],
            "Position": [
                f"{int(webster_stats['Position_Universe'].iloc[0])} out of {len(company_stats)}",
                f"{int(webster_stats['Position_Industry'].iloc[0])} out of {len(company_stats)}",  # Solo hay una industria en este caso
                "-",  # No hay subindustrias definidas en este caso
            ],
            "Percentile": [
                f"{int(webster_stats['Percentile_Universe'].iloc[0])}th",
                f"{int(webster_stats['Percentile_Industry'].iloc[0])}th",  # Solo hay una industria en este caso
                "-",  # No hay subindustrias definidas en este caso
            ],
        }
    )

    # Crear la tabla Dash
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in result_table.columns],
        data=result_table.to_dict("records"),
        style_cell={"textAlign": "left", "padding": "5px"},
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        style_table={"width": "100%", "margin": "auto"},
    )

    return table


def create_gauge_chart(score):
    """
    Creates a gauge chart based on the given score.

    Parameters:
    score (int): The score used to determine the category and value of the gauge chart.

    Returns:
    tuple: A tuple containing the created gauge chart (Figure object) and an explanation string.

    """
    fig = go.Figure()

    categories = [
        {"range": [0, 20], "color": "#8B0000", "text": "Very Low"},
        {"range": [21, 40], "color": "#FF6347", "text": "Low"},
        {"range": [41, 60], "color": "#FFFF00", "text": "Medium"},
        {"range": [61, 80], "color": "#90EE90", "text": "High"},
        {"range": [81, 100], "color": "#006400", "text": "Very High"},
    ]

    # Determine the category based on the score
    for cat in categories:
        if cat["range"][0] <= score <= cat["range"][1]:
            category = cat["text"]
            break

    steps = []
    for cat in categories:
        if cat["range"][0] <= score:
            steps.append({"range": cat["range"], "color": cat["color"]})
        else:
            steps.append(
                {"range": cat["range"], "color": "lightgrey"}
            )  # Neutro para categorías no alcanzadas

    fig.add_trace(
        go.Indicator(
            mode="gauge",
            value=score,
            domain={"x": [0.1, 1], "y": [0.2, 0.8]},
            gauge={
                "shape": "bullet",
                "axis": {
                    "range": [0, 100],
                    "tickmode": "array",
                    "tickvals": [],
                    "ticktext": [],
                    "tickwidth": 1,
                    "tickcolor": "darkblue",
                },
                "bar": {"color": "black"},
                "steps": steps,
                "threshold": {
                    "line": {"color": "black", "width": 2},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )
    if score <= 20:
        category = "Very Low"
        explanation = "This company exhibits a very low sentiment score. Approximately 80% of the feedback is negative, with only 20% being positive. This indicates significant dissatisfaction among respondents."
    elif score <= 40:
        category = "Low"
        explanation = "This company has a low sentiment score. Approximately 60% of the feedback is negative, while 40% is positive. This suggests a prevailing negative perception among respondents."
    elif score <= 60:
        category = "Medium"
        explanation = "This company holds a medium sentiment score. Feedback is evenly split, with 50% of comments being positive and 50% negative. This indicates a balanced perception among respondents."
    elif score <= 80:
        category = "High"
        explanation = "This company achieves a high sentiment score. Approximately 60% of the feedback is positive, compared to 40% negative. This reflects a generally favorable perception among respondents."
    else:
        category = "Very High"
        explanation = "This company has a very high sentiment score. Approximately 80% of the feedback is positive, with only 20% being negative. This indicates a strong positive perception among respondents."

    fig.update_layout(
        height=180,
        margin={"t": 40, "b": 20, "l": 40, "r": 20},
        annotations=[
            dict(
                x=0.19,
                y=0.25,
                text="Poor",
                showarrow=False,
                font=dict(size=12, color="white"),
                xanchor="center",
            ),
            dict(
                x=0.37,
                y=0.25,
                text="Low",
                showarrow=False,
                font=dict(size=12, color="white"),
                xanchor="center",
            ),
            dict(
                x=0.56,
                y=0.25,
                text="Medium",
                showarrow=False,
                font=dict(size=12, color="black"),
                xanchor="center",
            ),
            dict(
                x=0.73,
                y=0.25,
                text="Good",
                showarrow=False,
                font=dict(size=12, color="black"),
                xanchor="center",
            ),
            dict(
                x=0.9,
                y=0.25,
                text="Excellent",
                showarrow=False,
                font=dict(size=12, color="white"),
                xanchor="center",
            ),
            dict(
                x=0.19,
                y=0,
                text="[0-19]",
                showarrow=False,
                font=dict(size=12, color="black"),
                xanchor="center",
            ),
            dict(
                x=0.37,
                y=0,
                text="[20-39]",
                showarrow=False,
                font=dict(size=12, color="black"),
                xanchor="center",
            ),
            dict(
                x=0.56,
                y=0,
                text="[40-59]",
                showarrow=False,
                font=dict(size=12, color="black"),
                xanchor="center",
            ),
            dict(
                x=0.73,
                y=0,
                text="[60-79]",
                showarrow=False,
                font=dict(size=12, color="black"),
                xanchor="center",
            ),
            dict(
                x=0.9,
                y=0,
                text="[80-100]",
                showarrow=False,
                font=dict(size=12, color="black"),
                xanchor="center",
            ),
        ],
        title={
            "text": f"<b>{int(score)}</b><span style='color:lightgrey;'>/100</span> <b>{category}</b>",
            "y": 0.9,
            "x": 0.55,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 38},
        },
    )
    explanation_string = f"{category}. \n\n" f"{explanation}\n\n"

    return fig, explanation_string
def create_gauge_chart_ssindex(score, pillar_name):
    """
    Creates a gauge chart to visualize the score of a specific pillar.

    Parameters:
    score (int): The score of the pillar.
    pillar_name (str): The name of the pillar.

    Returns:
    fig (go.Figure): The gauge chart figure.
    """
    fig = go.Figure()

    categories = [
        {'range': [0, 20], 'color': "#8B0000", 'text': 'Very Low'},
        {'range': [21, 40], 'color': "#FF6347", 'text': 'Low'},
        {'range': [41, 60], 'color': "#FFFF00", 'text': 'Medium'},
        {'range': [61, 80], 'color': "#90EE90", 'text': 'High'},
        {'range': [81, 100], 'color': "#006400", 'text': 'Very High'}
    ]

    steps = []
    for cat in categories:
        if cat['range'][0] <= score:
            steps.append({'range': cat['range'], 'color': cat['color']})
        else:
            steps.append({'range': cat['range'], 'color': 'lightgrey'})  # Neutro para categorías no alcanzadas

    fig.add_trace(go.Indicator(
        mode="gauge",
        value=score,
        domain={'x': [0.1, 1], 'y': [0.2, 0.8]},
        gauge={
            'shape': "bullet",
            'axis': {
                'range': [0, 100],
                'tickmode': 'array',
                'tickvals': [],
                'ticktext': [],
                'tickwidth': 1,
                'tickcolor': 'darkblue'
            },
            'bar': {'color': "black"},
            'steps': steps,
            'threshold': {
                'line': {'color': "black", 'width': 2},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    if score <= 20:
        category = "Very Low"
    elif score <= 40:
        category = "Low"
    elif score <= 60:
        category = "Medium"
    elif score <= 80:
        category = "High"
    else:
        category = "Very High"

    fig.update_layout(
        height=120,
        margin={'t': 20, 'b': 10, 'l': 10, 'r': 0},
        annotations=[
            dict(x=0.19, y=0.25, text="Poor", showarrow=False, font=dict(size=12,color='white'), xanchor='center'),
            dict(x=0.37, y=0.25, text="Low", showarrow=False, font=dict(size=12, color='white'), xanchor='center'),
            dict(x=0.56, y=0.25, text="Medium", showarrow=False, font=dict(size=12, color='black'), xanchor='center'),
            dict(x=0.73, y=0.25, text="Good", showarrow=False, font=dict(size=12, color='black'), xanchor='center'),
            dict(x=0.9, y=0.25, text="Excellent", showarrow=False, font=dict(size=12, color='white'), xanchor='center'),
            dict(x=0.19, y=0, text="[0-19]", showarrow=False, font=dict(size=12,color='black'), xanchor='center'),
            dict(x=0.37, y=0, text="[20-39]", showarrow=False, font=dict(size=12, color='black'), xanchor='center'),
            dict(x=0.56, y=0, text="[40-59]", showarrow=False, font=dict(size=12, color='black'), xanchor='center'),
            dict(x=0.73, y=0, text="[60-79]", showarrow=False, font=dict(size=12, color='black'), xanchor='center'),
            dict(x=0.9, y=0, text="[80-100]", showarrow=False, font=dict(size=12, color='black'), xanchor='center')
        ],
        title={
            'text': f"<b>{int(score)}</b>",
            'y': 0.5,
            'x': 0.05,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18}
        }
    )

    return fig

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
df_grouped = (
    df1.groupby("state").agg({"Normalized_Sentiment_Score": "mean"}).reset_index()
)
general_score = df[df["Bank Name"] == bkn]["Total_Sentiment_Score"].mean()
general_gauge_chart, explanation_general_gauge_chart = create_gauge_chart(general_score)
industry_comments = df1[df1["Industry"] == "Banking"]
industry_comments["Sentiment_Category"] = industry_comments[
    "Normalized_Sentiment_Score"
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

fig_hist_general = px.bar(
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
fig_hist_general.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
fig_hist_general.update_layout(
    uniformtext_minsize=14,
)

score_by_pillar = df1.groupby('Predicted_SASB').agg(
    Avg_Score=('Normalized_Sentiment_Score', 'mean')
).reset_index()
pillars = score_by_pillar['Predicted_SASB'].unique()
# Crear gráficos de medidor para cada pilar

gauge_figures_2 = []

for index, row in score_by_pillar.iterrows():
    score = row['Avg_Score']
    pillar_name = row['Predicted_SASB']
    fig = create_gauge_chart_ssindex(score, pillar_name)
    gauge_figures_2.append(
        dbc.Row(
            [
                dbc.Col(
                    html.H4(pillar_name, style={'textAlign': 'left', 'padding-right': '20px'}),
                    width=2,
                    style={'display': 'flex', 'align-items': 'center'}
                ),
                dbc.Col(
                    dcc.Graph(figure=fig, config={'displayModeBar': False}),
                    width=10,
                    style={'padding-left': '0px'}
                )
            ],
            style={'margin-bottom': '0px', 'align-items': 'center'}
        )
    )    

score_by_pillar = df1.groupby('Pilar').agg(
    Avg_Score=('Normalized_Sentiment_Score', 'mean')
).reset_index()
pillars = score_by_pillar['Pilar'].unique()
gauge_figures_1 = []
for index, row in score_by_pillar.iterrows():
    score = row['Avg_Score']
    pillar_name = row['Pilar']
    fig = create_gauge_chart_ssindex(score, pillar_name)
    gauge_figures_1.append(
        dbc.Row(
            [
                dbc.Col(
                    html.H4(pillar_name, style={'textAlign': 'left', 'padding-right': '20px'}),
                    width=2,
                    style={'display': 'flex', 'align-items': 'center'}
                ),
                dbc.Col(
                    dcc.Graph(figure=fig, config={'displayModeBar': False}),
                    width=10,
                    style={'padding-left': '0px'}
                )
            ],
            style={'margin-bottom': '0px', 'align-items': 'center'}
        )
    )
    
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
                                    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'stretch'},
                                    children =gauge_figures_2)
                                    
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
                                    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'stretch'},
                                    children =gauge_figures_1)
                                    
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
