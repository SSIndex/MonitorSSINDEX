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


def categorize_score(score):
    if score <= 20:
        return "Poor"
    elif score <= 40:
        return "Low"
    elif score <= 60:
        return "Average"
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
        {"range": [0, 20], "color": "#8B0000", "text": "Very Low"},
        {"range": [21, 40], "color": "#FF6347", "text": "Low"},
        {"range": [41, 60], "color": "#FFFF00", "text": "Medium"},
        {"range": [61, 80], "color": "#90EE90", "text": "High"},
        {"range": [81, 100], "color": "#006400", "text": "Very High"},
    ]

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
        margin={"t": 20, "b": 10, "l": 10, "r": 0},
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
            "text": f"<b>{int(score)}</b>",
            "y": 0.5,
            "x": 0.05,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 18},
        },
    )

    return fig
