'''
GENERAL Analysis Layout
'''

# std imports

# 3rd party imports
from dash import html

# local imports
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
        {'range': [0, 20], 'color': "#8B0000", 'text': 'Very Low'},
        {'range': [21, 40], 'color': "#FF6347", 'text': 'Low'},
        {'range': [41, 60], 'color': "#FFFF00", 'text': 'Medium'},
        {'range': [61, 80], 'color': "#90EE90", 'text': 'High'},
        {'range': [81, 100], 'color': "#006400", 'text': 'Very High'}
    ]

    # Determine the category based on the score
    for cat in categories:
        if cat['range'][0] <= score <= cat['range'][1]:
            category = cat['text']
            break

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
        explanation = (
            "This company exhibits a very low sentiment score. Approximately 80% of the feedback is negative, with only 20% being positive. This indicates significant dissatisfaction among respondents."
        )
    elif score <= 40:
        category = "Low"
        explanation = (
            "This company has a low sentiment score. Approximately 60% of the feedback is negative, while 40% is positive. This suggests a prevailing negative perception among respondents."
        )
    elif score <= 60:
        category = "Medium"
        explanation = (
            "This company holds a medium sentiment score. Feedback is evenly split, with 50% of comments being positive and 50% negative. This indicates a balanced perception among respondents."
        )
    elif score <= 80:
        category = "High"
        explanation = (
            "This company achieves a high sentiment score. Approximately 60% of the feedback is positive, compared to 40% negative. This reflects a generally favorable perception among respondents."
        )
    else:
        category = "Very High"
        explanation = (
            "This company has a very high sentiment score. Approximately 80% of the feedback is positive, with only 20% being negative. This indicates a strong positive perception among respondents."
        )

    fig.update_layout(
        height=180,
        margin={'t': 40, 'b': 20, 'l': 40, 'r': 20},
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
            'text': f"<b>{int(score)}</b><span style='color:lightgrey;'>/100</span> <b>{category}</b>",
            'y': 0.9,
            'x': 0.55,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 38}
        }
    )
    explanation_string = (
        f"Monitor Overview: {category}\n\n"
        f"{explanation}\n\n"
    )

    return fig, explanation_string

bkn='Webster Bank'
df =pd.read_csv("MonitorSSINDEX/DashMonitor/data/data_procesa_inferencia_webster_SASB.csv")
df1 = df.copy()
filtro_general=(df['Pilar']=='Other') & (df['Predicted_SASB']=='Other')
df=df[filtro_general].reset_index(drop=True)
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
df_grouped = df1.groupby("state").agg({"Normalized_Sentiment_Score": "mean"}).reset_index()
general_score = df[df["Bank Name"] == bkn]["Total_Sentiment_Score"].mean()
general_gauge_chart, explanation_general_gauge_chart = create_gauge_chart(general_score)
GENERAL_ANALYSIS_LAYOUT = html.Div(
    className='container',
    children=[
        html.Section(
            className='section bg-light pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-12 justify-content-end',
                                    children=[
                                        html.P(
                                            children=[
                                                '2024-06-12'
                                            ]  # Here Goes the Date of last data extracted
                                        )
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-6',
                                    children=[
                                        html.Div(
                                            className='row',
                                            children=[
                                                html.H4(children=[bkn])
                                            ],  # Here goes Company Name
                                        ),
                                        html.Div(
                                            className='row',
                                            children=[
                                                html.P(
                                                    children=[
                                                        'Bank | EEUU | Market Name'
                                                    ]
                                                )
                                            ],  # Here goes Company Details
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className='col-6',
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
            className='section bg-white pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-2',
                                    children=[
                                        html.H6(
                                            className='text-end',
                                            children=['ESG COMPASS Overview:'],
                                        )
                                    ],
                                ),
                                html.Div(
                                    className='col-10',
                                    children=[
                                        html.P(
                                            className='text-center',
                                            children=[
                                                'HERE GOES THE OVERVIEW VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY LONG TEXT'
                                            ],
                                        )  # Here goes the overview description
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-6',
                                    children=[
                                        'HERE GOES SENTIMENT NORMALIZED HISTOGRAM (Y ranges from 0% to minimum between 100%, and max value of histogram )'
                                    ],
                                ),
                                html.Div(
                                    className='col-6',
                                    children=[
                                        'HERE GOES SENTIMENT RANKS TABLE',
                                        'POSICIÓN y PERCENTIL de: PROMEDIO UNIVERSO, PROMEDIO INDUSTRIA, SCORE EMPRESA',
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        html.Section(
            className='section bg-light pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        'Analisis SASB',
                        'Tabla con columnas: Pilar | Porcentaje Comentarios del Pilar con respecto a Total Comentarios Empresa | Score | Grafica Categorización'
                        'Añadir Pilar Otros: Comentarios que no caen dentro de los pilares del análisis de ASG',
                    ],
                )
            ],
        ),
        html.Section(
            className='section bg-white pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        'Analisis SSINDEX',
                        'Mismos comentarios que análisis SASB',
                    ],
                )
            ],
        ),
        html.Section(
            className='section bg-light pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        'Analisis Detallado SASB',
                        'Columnas: Dimension | Porcentaje Comentarios del Pilar con respecto a Total | Puntaje | Categorizacion',
                    ],
                )
            ],
        ),
        html.Section(
            className='section bg-white pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        'Analisis Detallado SSINDEX',
                        'Mismos comentarios de Analisis detallado SASB',
                    ],
                )
            ],
        ),
    ],
)
