import dash
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def sentiment_color(score):
    if score <= 50:
        return 'red'
    elif score <= 75:
        return 'yellow'
    else:
        return 'green'

df = pd.read_csv("data/processed_webster.csv")
df['Nuevo_Sentiment_Score'] = df['Smoothed_Sentiment_Score']
df['ds'] = pd.to_datetime(df['ds'])
df1 = df.copy()

month_map = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}

df['month_num'] = df['month'].map(month_map)
df = df.groupby(["Bank Name", "Predicted_Pilar", "year", "month_num"])[["Nuevo_Sentiment_Score"]].mean().reset_index()
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month_num'].map('{:02}'.format), format='%Y-%m')
df['Total_Sentiment_Score'] = df.groupby(['Bank Name', 'date'])['Nuevo_Sentiment_Score'].transform('mean')
df.sort_values('date', inplace=True)

state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI',
    'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
    'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
    'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
    'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

df1['state'] = df1['state'].map(state_abbrev)
df_grouped = df1.groupby('state').agg({'Sentiment_Score': 'mean'}).reset_index()
df_grouped['color'] = df_grouped['Sentiment_Score'].apply(sentiment_color)
colorscale = [[0, 'red'], [0.5, 'yellow'], [1, 'green']]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de la aplicación
app.layout = html.Div([
    html.Div([
        html.Img(src='assets/ssindex.png', style={'height': '60px', 'margin': '10px'}),
        html.Div(id='selected-bank', style={'font-size': '20px', 'font-weight': 'bold', 'margin': '10px'}),
        html.Div([
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year} for year in df['year'].unique()],
                value=df['year'].max(),
                clearable=False
            ),
            dcc.Dropdown(
                id='pilar-dropdown',
                options=[{'label': pilar, 'value': pilar} for pilar in df['Predicted_Pilar'].unique()],
                value=df['Predicted_Pilar'].unique()[0],
                clearable=False
            ),
            dcc.Dropdown(
                id='bank-dropdown',
                options=[{'label': bank, 'value': bank} for bank in df['Bank Name'].unique()],
                value=df['Bank Name'].unique()[0],
                clearable=False
            ),
        ], style={'padding':'20px'}),
    ], ),
    html.Div([
        dcc.Graph(id='line-chart'),
        dcc.Graph(id='us-map'),
        html.Div(id='review-table-container')
    ]),
    html.Div([
        dcc.Checklist(
            id='bank-checklist',
            options=[{'label': name, 'value': name} for name in df['Bank Name'].unique()],
            value=['Webster Bank'],
            inline=True
        )
    ], style={'padding': '20px'}),
    dcc.Graph(id='yearly-pilar-line-plot'),
    dcc.Graph(id='total-score-line-plot'),
    dcc.Graph(id='overall-time-line-plot'),
    dcc.Graph(id='sentiment-heatmap'),
    dcc.Graph(id='bubble-chart'),
    dcc.Graph(id='boxplot-chart'),
    dcc.Graph(id='violin-chart'),
])

# Callbacks para actualizar los gráficos y la tabla
@app.callback(
    Output('line-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('pilar-dropdown', 'value'),
     Input('bank-dropdown', 'value')]
)
def update_line_chart(selected_year, selected_pilar, selected_bank):
    filtered_df = df[(df['year'] == selected_year) & 
                     (df['Predicted_Pilar'] == selected_pilar) & 
                     (df['Bank Name'] == selected_bank)]
    fig = px.line(filtered_df, x='date', y='Total_Sentiment_Score', title='Sentiment Over Time')
    return fig

@app.callback(
    [Output('us-map', 'figure'), Output('review-table-container', 'children')],
    [Input('year-dropdown', 'value'),
     Input('pilar-dropdown', 'value'),
     Input('bank-dropdown', 'value'),
     Input('us-map', 'clickData')]
)
def update_us_map(selected_year, selected_pilar, selected_bank, click_data):
    filtered_df = df1[(df1['year'] == selected_year) & 
                      (df1['Predicted_Pilar'] == selected_pilar) & 
                      (df1['Bank Name'] == selected_bank)]
    df_grouped = filtered_df.groupby('state').agg({'Sentiment_Score': 'mean'}).reset_index()
    df_grouped['color'] = df_grouped['Sentiment_Score'].apply(sentiment_color)
    
    fig = go.Figure(data=go.Choropleth(
        locations=df_grouped['state'],
        z=df_grouped['Sentiment_Score'],
        locationmode='USA-states',
        colorscale=colorscale,
        marker_line_color='white'
    ))
    fig.update_layout(
        title_text='Average Sentiment Score by State',
        geo_scope='usa',
    )
    reviews_table = html.Table()
    if click_data:
        state = click_data['points'][0]['location']
        reviews = filtered_df[filtered_df['state'] == state][['Review', 'Sentiment_Score', 'Bank Name']].head(5)
        reviews_table = html.Table(
            [
                html.Thead(
                    html.Tr([html.Th(col, style={'padding': '10px', 'border': '1px solid black'}) for col in reviews.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(reviews.iloc[i][col], style={'padding': '10px', 'border': '1px solid black'}) for col in reviews.columns
                    ]) for i in range(len(reviews))
                ])
            ],
            style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '20px'}
        )
    return fig, reviews_table

@app.callback(
    [Output('yearly-pilar-line-plot', 'figure'),
     Output('total-score-line-plot', 'figure'),
     Output('overall-time-line-plot', 'figure'),
     Output('sentiment-heatmap', 'figure'),
     Output('bubble-chart', 'figure'),
     Output('boxplot-chart', 'figure'),
     Output('violin-chart', 'figure'),
     Output('selected-bank', 'children')],
    [Input('year-dropdown', 'value'),
     Input('pilar-dropdown', 'value'),
     Input('bank-checklist', 'value')]
)
def update_graphs(selected_year, selected_pilar, selected_banks):
    filtered_df = df[(df['year'] == selected_year) & 
                     (df['Predicted_Pilar'] == selected_pilar) & 
                     (df['Bank Name'].isin(selected_banks))]

    yearly_pilar_line_fig = px.line(filtered_df, x='date', y='Nuevo_Sentiment_Score', color='Bank Name', title=f'Sentiment Score for {selected_year} - {selected_pilar}')
    yearly_pilar_line_fig.update_layout(
        font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
    )
    total_score_line_fig = px.line(filtered_df, x='date', y='Total_Sentiment_Score', color='Bank Name', title=f'Total Sentiment Score for {selected_year}')
    total_score_line_fig.update_layout(
        font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
    )
    overall_df = df[df['Bank Name'].isin(selected_banks)].groupby(['Bank Name','date']).agg({'Total_Sentiment_Score': 'mean'}).reset_index()
    overall_time_line_fig = px.line(overall_df, x='date', y='Total_Sentiment_Score',color='Bank Name', title='Overall Sentiment Score Over Time')
    overall_time_line_fig.update_layout(
        font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
    )
    
    start_date = '2016-04-30'
    df_filtered = df1[df1['ds'] >= start_date]
    df_grouped_1 = df_filtered.groupby(['Bank Name', pd.Grouper(key='ds', freq='ME')])['Nuevo_Sentiment_Score'].mean().reset_index()
    df_pivot = df_grouped_1.pivot(index='Bank Name', columns='ds', values='Nuevo_Sentiment_Score')
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=df_pivot.values,
        x=df_pivot.columns,
        y=df_pivot.index,
        colorscale='Viridis',
        colorbar=dict(title='Average Sentiment Score')
    ))
    heatmap_fig.update_layout(
        title='Heatmap of Average Sentiment Scores',
        xaxis_nticks=36
    )
    
    filtered_df_2 =df[(df['Bank Name'].isin(selected_banks))]
    filtered_df_2 = filtered_df_2.groupby(['Bank Name', 'year']).agg({
        'Nuevo_Sentiment_Score': 'mean',
        'Total_Sentiment_Score': 'mean'
    }).reset_index()
    
    bubble_fig = px.scatter(filtered_df_2, x='year', y='Nuevo_Sentiment_Score', size='Total_Sentiment_Score', color='Bank Name', title='Bubble Chart')
    bubble_fig.update_layout(
        font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
    )
    
    boxplot_fig = px.box(filtered_df, x='Bank Name', y='Nuevo_Sentiment_Score', color='Bank Name', title='Boxplot of Sentiment Scores by Bank')
    violin_fig = px.violin(filtered_df, x='Bank Name', y='Nuevo_Sentiment_Score', color='Bank Name', title='Violin Plot of Sentiment Scores by Bank')
    
    selected_bank_text = f"Currently Evaluating: {', '.join(selected_banks)}"

    return (yearly_pilar_line_fig, total_score_line_fig, overall_time_line_fig, heatmap_fig, bubble_fig, boxplot_fig, violin_fig,selected_bank_text)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
