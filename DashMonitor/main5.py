import dash
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
category_order = ['Universe', 'Industry', 'Company']
custom_colors = {
    'Universe': '#1f77b4',  # Blue
    'Industry': '#2ca02c',  # Green
    'Company': '#ff7f0e'    # Orange
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
def sentiment_color(score):
    if score <= 50:
        return "red"
    elif score <= 75:
        return "yellow"
    else:
        return "green"
def create_result_table(data):
    # Calcular el total de comentarios y el promedio del puntaje para cada compañía
    company_stats = data.groupby('Bank Name').agg(
        Total_Comments=('Normalized_Sentiment_Score', 'size'),
        Avg_Score=('Normalized_Sentiment_Score', 'mean')
    ).reset_index()

    # Ordenar por el puntaje promedio
    company_stats = company_stats.sort_values(by='Avg_Score', ascending=False).reset_index(drop=True)

    # Calcular la posición de la compañía en el universo y la industria
    company_stats['Position_Universe'] = company_stats.index + 1
    company_stats['Position_Industry'] = company_stats.index + 1  # Solo hay una industria en este caso

    # Calcular el percentil de la compañía
    company_stats['Percentile_Universe'] = company_stats['Avg_Score'].rank(pct=True) * 100
    company_stats['Percentile_Industry'] = company_stats['Avg_Score'].rank(pct=True) * 100  # Solo hay una industria en este caso

    # Filtrar los datos para la tabla final
    webster_stats = company_stats[company_stats['Bank Name'] == 'Webster Bank']

    # Crear la tabla de resultados
    result_table = pd.DataFrame({
        'Type': ['Global Universe', 'Technology Hardware (Industry)', 'Communications Equipment (Subindustry)'],
        'Position': [
            f"{int(webster_stats['Position_Universe'].iloc[0])} out of {len(company_stats)}",
            f"{int(webster_stats['Position_Industry'].iloc[0])} out of {len(company_stats)}",  # Solo hay una industria en este caso
            '-'  # No hay subindustrias definidas en este caso
        ],
        'Percentile': [
            f"{int(webster_stats['Percentile_Universe'].iloc[0])}th",
            f"{int(webster_stats['Percentile_Industry'].iloc[0])}th",  # Solo hay una industria en este caso
            '-'  # No hay subindustrias definidas en este caso
        ]
    })

    # Crear la tabla Dash
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in result_table.columns],
        data=result_table.to_dict('records'),
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_table={'width': '100%', 'margin': 'auto'}
    )
    
    return table
def create_gauge_chart_ssindex(score, pillar_name):
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
    
def create_gauge_chart(score):
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

bkn="Webster Bank"
df =pd.read_csv("data/data_procesa_inferencia_webster_SASB.csv")
df['Industry'] = 'Banking'
df["Nuevo_Sentiment_Score"] = df["Normalized_Sentiment_Score"]                
df["ds"] = pd.to_datetime(df["ds"])
df['Sentiment_Category'] = df['Normalized_Sentiment_Score'].apply(categorize_score)
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
filtro_general=(df['Pilar']=='Other') & (df['Predicted_SASB']=='Other')
df=df[filtro_general].reset_index(drop=True)
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
df_grouped = df1.groupby("state").agg({"Normalized_Sentiment_Score": "mean"}).reset_index()
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
filtro_sasb=df1['Predicted_SASB']=='Other'
df_sasb=df1[filtro_sasb]
df_sasb.reset_index(drop=True,inplace=True)
filtro_ssindex=df1['Pilar']=='Other'
df_ssindex=df1[filtro_ssindex]
df_ssindex.reset_index(drop=True,inplace=True)

aux=df1[df1["Bank Name"] == bkn]
aux=aux[filtro_general]
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
    

industry_comments = df1[df1['Industry'] == 'Banking']
industry_comments['Sentiment_Category'] = industry_comments['Normalized_Sentiment_Score'].apply(categorize_score)
universe_totals = df1['Sentiment_Category'].value_counts(normalize=True) * 100
industry_totals = industry_comments['Sentiment_Category'].value_counts(normalize=True) * 100
obj_bank = df1[df1['Bank Name'] == bkn]
total_obj_bank = len(obj_bank)
obj_bank_totals_corrected =obj_bank['Sentiment_Category'].value_counts(normalize=True) * 100
percentage_data_corrected = []
for category in ['Poor', 'Low', 'Medium', 'Good', 'Excellent']:
    percentage_data_corrected.append({
        'Category': category,
        'Type': 'Universe',
        'Percentage': universe_totals.get(category, 0)
    })
    percentage_data_corrected.append({
        'Category': category,
        'Type': 'Industry',
        'Percentage': industry_totals.get(category, 0)
    })
    percentage_data_corrected.append({
        'Category': category,
        'Type': 'Company',
        'Percentage': obj_bank_totals_corrected.get(category, 0),
        'Company': 'Webster Bank'
    })

percentage_df_corrected = pd.DataFrame(percentage_data_corrected)
percentage_df_corrected['Category'] = pd.Categorical(percentage_df_corrected['Category'], categories=['Poor', 'Low', 'Medium', 'Good', 'Excellent'], ordered=True)
percentage_df_corrected = percentage_df_corrected.sort_values('Category')

fig_hist_general=px.bar(percentage_df_corrected, x='Category', y='Percentage', color='Type', barmode='group',
                       text='Percentage', height=400, category_orders={"Type": category_order}, color_discrete_map=custom_colors)
fig_hist_general.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig_hist_general.update_layout(uniformtext_minsize=14,)


industry_comments = df_sasb[df_sasb['Industry'] == 'Banking']
industry_comments['Sentiment_Category'] = industry_comments['Normalized_Sentiment_Score'].apply(categorize_score)
universe_totals = df_sasb['Sentiment_Category'].value_counts(normalize=True) * 100
industry_totals = industry_comments['Sentiment_Category'].value_counts(normalize=True) * 100
obj_bank = df_sasb[df_sasb['Bank Name'] == bkn]
total_obj_bank = len(obj_bank)
obj_bank_totals_corrected =obj_bank['Sentiment_Category'].value_counts(normalize=True) * 100
percentage_data_corrected = []
for category in ['Poor', 'Low', 'Medium', 'Good', 'Excellent']:
    percentage_data_corrected.append({
        'Category': category,
        'Type': 'Universe',
        'Percentage': universe_totals.get(category, 0)
    })
    percentage_data_corrected.append({
        'Category': category,
        'Type': 'Industry',
        'Percentage': industry_totals.get(category, 0)
    })
    percentage_data_corrected.append({
        'Category': category,
        'Type': 'Company',
        'Percentage': obj_bank_totals_corrected.get(category, 0),
        'Company': 'Webster Bank'
    })

percentage_df_corrected = pd.DataFrame(percentage_data_corrected)
percentage_df_corrected['Category'] = pd.Categorical(percentage_df_corrected['Category'], categories=['Poor', 'Low', 'Medium', 'Good', 'Excellent'], ordered=True)
percentage_df_corrected = percentage_df_corrected.sort_values('Category')

fig_hist_sasb=px.bar(percentage_df_corrected, x='Category', y='Percentage', color='Type', barmode='group',
                       text='Percentage', height=400, category_orders={"Type": category_order}, color_discrete_map=custom_colors)
fig_hist_sasb.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig_hist_sasb.update_layout(uniformtext_minsize=14,)

industry_comments = df_ssindex[df_ssindex['Industry'] == 'Banking']
industry_comments['Sentiment_Category'] = industry_comments['Normalized_Sentiment_Score'].apply(categorize_score)
universe_totals = df_ssindex['Sentiment_Category'].value_counts(normalize=True) * 100
industry_totals = industry_comments['Sentiment_Category'].value_counts(normalize=True) * 100
obj_bank = df_ssindex[df_ssindex['Bank Name'] == bkn]
total_obj_bank = len(obj_bank)
obj_bank_totals_corrected =obj_bank['Sentiment_Category'].value_counts(normalize=True) * 100
percentage_data_corrected = []
for category in ['Poor', 'Low', 'Medium', 'Good', 'Excellent']:
    percentage_data_corrected.append({
        'Category': category,
        'Type': 'Universe',
        'Percentage': universe_totals.get(category, 0)
    })
    percentage_data_corrected.append({
        'Category': category,
        'Type': 'Industry',
        'Percentage': industry_totals.get(category, 0)
    })
    percentage_data_corrected.append({
        'Category': category,
        'Type': 'Company',
        'Percentage': obj_bank_totals_corrected.get(category, 0),
        'Company': 'Webster Bank'
    })

percentage_df_corrected = pd.DataFrame(percentage_data_corrected)
percentage_df_corrected['Category'] = pd.Categorical(percentage_df_corrected['Category'], categories=['Poor', 'Low', 'Medium', 'Good', 'Excellent'], ordered=True)
percentage_df_corrected = percentage_df_corrected.sort_values('Category')
fig_hist_ssindex=px.bar(percentage_df_corrected, x='Category', y='Percentage', color='Type', barmode='group',
                       text='Percentage', height=400, category_orders={"Type": category_order}, color_discrete_map=custom_colors)
fig_hist_ssindex.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig_hist_ssindex.update_layout(uniformtext_minsize=14,)
general_score = df[df["Bank Name"] == bkn]["Total_Sentiment_Score"].mean()
df_2=df_sasb.copy()
df_2["month_num"] = df_sasb["month"].map(month_map)
df_2 = (
    df_2.groupby(["Bank Name", "Predicted_Pilar", "year", "month_num"])[
        ["Nuevo_Sentiment_Score"]
    ]
    .mean()
    .reset_index()
)
df_2["date"] = pd.to_datetime(
    df_2["year"].astype(str) + "-" + df_2["month_num"].map("{:02}".format), format="%Y-%m"
)
df_2["Total_Sentiment_Score"] = df_2.groupby(["Bank Name", "date"])[
    "Nuevo_Sentiment_Score"
].transform("mean")
df_2.sort_values("date", inplace=True)
sasb_score = df_2[df_2["Bank Name"] == bkn]['Total_Sentiment_Score'].mean()
df_3=df_ssindex.copy()
df_3["month_num"] = df_ssindex["month"].map(month_map)
df_3 = (
    df_3.groupby(["Bank Name", "Predicted_Pilar", "year", "month_num"])[
        ["Nuevo_Sentiment_Score"]
    ]
    .mean()
    .reset_index()
)
df_3["date"] = pd.to_datetime(
    df_3["year"].astype(str) + "-" + df_3["month_num"].map("{:02}".format), format="%Y-%m"
)
df_3["Total_Sentiment_Score"] = df_3.groupby(["Bank Name", "date"])[
    "Nuevo_Sentiment_Score"
].transform("mean")
df_3.sort_values("date", inplace=True)
ssindex_score = df_3[df_3["Bank Name"] == bkn]['Total_Sentiment_Score'].mean()
general_gauge_chart, explanation_general_gauge_chart = create_gauge_chart(general_score)
sasb_gauge_chart, explanation_sasb_gauge_chart = create_gauge_chart(sasb_score)
ssindex_gauge_chart, explanation_ssindex_gauge_chart = create_gauge_chart(ssindex_score)

fig_risk_sasb = go.Figure()
fig_risk_sasb.add_shape(type="rect", x0=0, y0=50, x1=1, y1=100,
              fillcolor="lightgreen", opacity=0.5, line_width=0)
fig_risk_sasb.add_shape(type="rect", x0=0, y0=0, x1=1, y1=50,
              fillcolor="lightcoral", opacity=0.5, line_width=0)
for sentiment in df_sasb['Sentiment_gen'].unique():
    filtered_df_1 = df_sasb[df_sasb['Sentiment_gen'] == sentiment]
    fig_risk_sasb.add_trace(go.Scatter(
        x=filtered_df_1['Total_Count'],
        y=filtered_df_1['Normalized_Sentiment_Score'],
        mode='markers',
        name=sentiment,
        marker=dict(
            size=6,
            line=dict(width=1)
        )
    ))
fig_risk_sasb.update_layout(
    title="Sentiment vs Exposure and Management",
    xaxis_title="Exposure (Total_Count)",
    yaxis_title="Sentiment (Normalized_Sentiment_Score)",
    showlegend=True,
    annotations=[
        dict(
            x=0.1,
            y=0.95,
            text="Weak",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black")
        ),
        dict(
            x=0.1,
            y=0.05,
            text="Strong",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black")
        ),
        dict(
            x=0.05,
            y=0.5,
            text="Sentiment",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black"),
            textangle=-90
        ),
        dict(
            x=0.5,
            y=0.02,
            text="Low",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black")
        ),
        dict(
            x=0.95,
            y=0.02,
            text="High",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black")
        ),
        dict(
            x=0.95,
            y=0.95,
            text="Severe Risk",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black")
        ),
        dict(
            x=0.95,
            y=0.05,
            text="Negligible Risk",
            showarrow=False,
            xref="paper",
            yref="paper",
            font=dict(size=12, color="black")
        )
    ]
)


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
    xaxis=dict(
        showgrid=True,
        tickformat='%d-%b',
        tickangle=-45
    ),
    yaxis=dict(showgrid=True),
    updatemenus=[
        {
            "buttons": [
                {
                    "args": [
                        {
                            "xaxis": {
                                "range": [overall_df['date'].max() - pd.Timedelta(days=7), overall_df['date'].max()],
                                "tickformat": '%d-%b',
                                "tickangle" : -45
                            }
                        }
                    ],
                    "label": "1 Semana",
                    "method": "relayout"
                },
                {
                    "args": [
                        {
                            "xaxis": {
                                "range": [overall_df['date'].max() - pd.Timedelta(days=30), overall_df['date'].max()],
                                "tickformat": '%d-%b',
                                "tickangle" : -45
                            }
                        }
                    ],
                    "label": "1 Mes",
                    "method": "relayout"
                },
                {
                    "args": [
                        {
                            "xaxis": {
                                "range": [overall_df['date'].max() - pd.Timedelta(days=182), overall_df['date'].max()],
                                "tickformat": '%b-%Y',
                                "tickangle" : -45
                            }
                        }
                    ],
                    "label": "6 Meses",
                    "method": "relayout"
                },
                {
                    "args": [
                        {
                            "xaxis": {
                                "range": [overall_df['date'].max() - pd.Timedelta(days=365), overall_df['date'].max()],
                                "tickformat": '%b-%Y',
                                "tickangle" : -45
                            }
                        }
                    ],
                    "label": "1 Año",
                    "method": "relayout"
                },
                {
                    "args": [
                        {
                            "xaxis": {
                                "range": [overall_df['date'].max() - pd.Timedelta(days=1095), overall_df['date'].max()],
                                "tickformat": '%b-%Y',
                                "tickangle" : -45
                            }
                        }
                    ],
                    "label": "3 Años",
                    "method": "relayout"
                },
                {
                    "args": [
                        {
                            "xaxis": {
                                "range": [overall_df['date'].min(), overall_df['date'].max()],
                                "tickformat":'%b-%Y',
                                "tickangle" : -45
                            }
                        }
                    ],
                    "label": "Toda la historia",
                    "method": "relayout"
                }
            ],
            "direction": "left",
            "showactive": True,
            "x": 0.5,
            "xanchor": "center",
            "y": 1,
            "yanchor": "top",
            "type": "buttons"
        }
    ]
    )
    boxplot_fig = px.box(
        filtered_df,
        x="Bank Name",
        y="Nuevo_Sentiment_Score",
        color="Bank Name",
        title="Boxplot of Sentiment Scores by Bank",
    )


    return (
        overall_time_line_fig,
        boxplot_fig,
    )
@app.callback(
    [Output("sasb-map", "figure"), Output("sasb-table", "children")],
    [
        Input("sasb-map", "clickData"),
    ],
)
def update_sasb_map(click_data):
    filtered_df=df_sasb.copy()
    filtered_df=filtered_df[filtered_df['Bank Name'] == bkn]
    df_grouped = (
        filtered_df.groupby("state").agg({"Sentiment_Score": "mean"}).reset_index()
    )
    df_grouped["color"] = df_grouped["Sentiment_Score"].apply(sentiment_color)

    fig = go.Figure(
        data=go.Choropleth(
            locations=df_grouped["state"],
            z=df_grouped["Sentiment_Score"],
            locationmode="USA-states",
            colorscale=colorscale,
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
                                style={"padding": "10px", "border": "1px solid black"},
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
            style={"width": "100%", "borderCollapse": "collapse", "marginTop": "20px"},
        )
    return fig, reviews_table
@app.callback(
    [Output("ssindex-map", "figure"), Output("ssindex-table", "children")],
    [
        Input("ssindex-map", "clickData"),
    ],
)
def update_ssindex_map(click_data):
    filtered_df=df_ssindex.copy()
    filtered_df=filtered_df[filtered_df['Bank Name'] == bkn]
    df_grouped = (
        filtered_df.groupby("state").agg({"Sentiment_Score": "mean"}).reset_index()
    )
    df_grouped["color"] = df_grouped["Sentiment_Score"].apply(sentiment_color)

    fig = go.Figure(
        data=go.Choropleth(
            locations=df_grouped["state"],
            z=df_grouped["Sentiment_Score"],
            locationmode="USA-states",
            colorscale=colorscale,
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
                                style={"padding": "10px", "border": "1px solid black"},
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
            style={"width": "100%", "borderCollapse": "collapse", "marginTop": "20px"},
        )
    return fig, reviews_table

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
                                                    html.P(
                                                        "Bank | EEUU | Market Name"
                                                    )
                                                ),
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                id="gauge-chart", figure=general_gauge_chart
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
                                dbc.Row(  html.P(
                                               explanation_general_gauge_chart
                                            )),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [ 
                                                dcc.Graph(id='histogram', figure=fig_hist_general)                                               
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(
                                            create_result_table(df1),
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
                                dbc.Row(  html.H1("Analisis SASB", style={'textAlign': 'justify'})),
                                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                gauge_figures_2,
                                style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'stretch'}
                            ),
                            width=12
                        )
                    ]
                )
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
                                dbc.Row(  html.H1("Analisis SSINDEX", style={'textAlign': 'justify'})),
                                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                gauge_figures_1,
                                style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'stretch'}
                            ),
                            width=12
                        )
                    ]
                )
                            ],
                        )
                    ],
                ),
            ]
        )
    elif tab == "sasb":
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
                                                    html.P(
                                                        "Bank | EEUU | Market Name"
                                                    )
                                                ),
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                id="gauge-chart", figure=sasb_gauge_chart
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
                                dbc.Row(  html.P(
                                               explanation_sasb_gauge_chart
                                            )),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [ 
                                                dcc.Graph(id='histogram', figure=fig_hist_sasb)                                               
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(
                                            create_result_table(df1),
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
                                dbc.Row(  html.H1("Analisis SASB", style={'textAlign': 'justify'})),
                                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                gauge_figures_2,
                                style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'stretch'}
                            ),
                            width=12
                        )
                    ]
                )
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
                                dbc.Row(  html.H1("Analisis Geografico Pilar SASB", style={'textAlign': 'justify'})),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [ 
                                                dcc.Graph(id='sasb-map')                                               
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(html.Div(id="sasb-table"), width=6)
                                    ],
                                        ),
                                    ]
                                ),
                            ],
                        ),
                html.Div(
                    className="section bg-white",
                    children=[
                        dbc.Container(
                            className="border-bottom border-dark",
                            children=[
                                dbc.Row(  html.H1("Analisis De Impacto y Riesgo SASB", style={'textAlign': 'justify'})),
                                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(figure=fig_risk_sasb),
                            width=12
                        )
                    ]
                )
                            ],
                        )
                    ],
                )
                    ],
                )
    elif tab == "ssindex":
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
                                                    html.P(
                                                        "Bank | EEUU | Market Name"
                                                    )
                                                ),
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                id="gauge-chart", figure=ssindex_gauge_chart
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
                                dbc.Row(  html.P(
                                               explanation_ssindex_gauge_chart
                                            )),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [ 
                                                dcc.Graph(id='histogram', figure=fig_hist_ssindex)                                               
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(
                                            create_result_table(df1),
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
                                dbc.Row(  html.H1("Analisis SSINDEX", style={'textAlign': 'justify'})),
                                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                gauge_figures_1,
                                style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'stretch'}
                            ),
                            width=12
                        )
                    ]
                )
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
                                dbc.Row(  html.H1("Analisis Geografico Pilar SSINDEX", style={'textAlign': 'justify'})),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [ 
                                                dcc.Graph(id='ssindex-map')                                               
                                            ],
                                            width=6,
                                        ),
                                        dbc.Col(html.Div(id="ssindex-table"), width=6)
                                    ],
                                        ),
                                    ]
                                ),
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
                                            [ 
                                                dcc.Graph(id='overall-time-line-plot')                                               
                                            ],
                                            width=8,
                                        ),
                                        dbc.Col(
                    [
                        html.Img(
                            src="assets/ssindex.png",
                            style={"height": "60px", "margin": "10px"},
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
                                        for pilar in df["Predicted_Pilar"].unique()
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
                                        )
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
                                            [
                                                 dcc.Graph(id='boxplot-chart') 
                                            ],
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

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8052)
