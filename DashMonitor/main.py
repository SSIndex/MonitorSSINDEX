import plotly.express as px
import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objects as go

def sentiment_color(score):
    if score <= 50:
        return 'red'
    elif score <= 75:
        return 'yellow'
    else:
        return 'green'
df = pd.read_csv("data/processed_webster.csv")
df['Nuevo_Sentiment_Score']=df['Smoothed_Sentiment_Score']
df['ds'] = pd.to_datetime(df['ds'])
df1=df
month_map = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}
df['month_num'] = df['month'].map(month_map)
df=df.groupby(["Bank Name","Predicted_Pilar","year","month_num"])[["Nuevo_Sentiment_Score"]].mean().reset_index()
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

app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.Div[
        html.Button("Cambiar Tema", id="theme-button", n_clicks=0),
        html.Img(src='assets/ssindex.png', style={'height': '60px', 'margin': '10px'}),
        html.H1("Monitor SSINDEX", id="title", style={'text-align': 'center', 'font-family': 'Roboto'}),
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
        dcc.Graph(id='geo-chart'),
        html.Div(id='review-table-container')
    ], id='main-container')
])

# Callback para actualizar los gráficos y manejar el tema
@app.callback(
    [Output('yearly-pilar-line-plot', 'figure'),
     Output('total-score-line-plot', 'figure'),
     Output('overall-time-line-plot', 'figure'),
     Output('main-container', 'style'),
     Output('title', 'style'),
     Output('sentiment-heatmap', 'figure'),
     Output('bubble-chart', 'figure'),
     Output('boxplot-chart', 'figure'),
     Output('geo-chart', 'figure'),],
    [Input('year-dropdown', 'value'),
     Input('pilar-dropdown', 'value'),
     Input('bank-checklist', 'value'),
     Input('theme-button', 'n_clicks')],
    [State('main-container', 'style')]
)
def update_graphs(selected_year, selected_pilar, selected_banks, n_clicks, style):
    dark_theme = n_clicks % 2 != 0
    container_style = {
        'backgroundColor': '#333' if dark_theme else '#FFF',
        'padding': '20px',
        'borderRadius': '15px',
        'boxShadow': '0px 0px 10px #000'
    }
    title_style = {'text-align': 'center', 'color': 'white' if dark_theme else 'black'}

    filtered_df = df[(df['year'] == selected_year) & (df['Predicted_Pilar'] == selected_pilar) & (df['Bank Name'].isin(selected_banks))]
    filtered_df_2 =df[(df['Bank Name'].isin(selected_banks))]
    start_date = '2016-04-30'
    df_filtered = df1[df1['ds'] >= start_date]
    df_grouped_1 = df_filtered.groupby(['Bank Name', pd.Grouper(key='ds', freq='ME')])['Nuevo_Sentiment_Score'].mean().reset_index()
    df_pivot = df_grouped_1.pivot(index='Bank Name', columns='ds', values='Nuevo_Sentiment_Score')
    df_grouped = df1.groupby('state').agg({'Sentiment_Score': 'mean'}).reset_index()
    df_grouped['color'] = df_grouped['Sentiment_Score'].apply(sentiment_color)
    color_scale = [[0, 'red'], [0.5, 'yellow'], [1, 'green']]
    
    fig_pilar = px.line(filtered_df, x='date', y='Nuevo_Sentiment_Score', color='Bank Name', title=f'Sentiment Score for {selected_year} - {selected_pilar}')
    fig_pilar.update_layout(
        plot_bgcolor=container_style['backgroundColor'],
        font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
        paper_bgcolor=container_style['backgroundColor'],
        font_color=title_style['color']
    )

    fig_total_yearly = px.line(filtered_df, x='date', y='Total_Sentiment_Score', color='Bank Name', title=f'Total Sentiment Score for {selected_year}')
    fig_total_yearly.update_layout(
        plot_bgcolor=container_style['backgroundColor'],
        font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
        paper_bgcolor=container_style['backgroundColor'],
        font_color=title_style['color']
    )

    overall_df = df[df['Bank Name'].isin(selected_banks)].groupby(['Bank Name','date']).agg({'Total_Sentiment_Score': 'mean'}).reset_index()
    fig_overall = px.line(overall_df, x='date', y='Total_Sentiment_Score', color='Bank Name', title='Overall Sentiment Score Over Time')
    fig_overall.update_layout(
        plot_bgcolor=container_style['backgroundColor'],
        paper_bgcolor=container_style['backgroundColor'],
        font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
        font_color=title_style['color']
    )
    
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
    bubble_fig = px.scatter(filtered_df_2, x='date', y='Nuevo_Sentiment_Score', size='Total_Sentiment_Score', color='Bank Name', title='Bubble Chart of Sentiments')
    bubble_fig.update_layout(
        plot_bgcolor=container_style['backgroundColor'],
        paper_bgcolor=container_style['backgroundColor'],
        font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
        font_color=title_style['color']
    )

    boxplot_fig = px.box(filtered_df, x='Bank Name', y='Nuevo_Sentiment_Score', color='Bank Name', title='Boxplot of Sentiment Scores by Bank')
    boxplot_fig.update_layout(
        plot_bgcolor=container_style['backgroundColor'],
        paper_bgcolor=container_style['backgroundColor'],
        font=dict(family="Roboto"),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
        font_color=title_style['color']
    )

    geobar_fig=go.Figure(data=go.Choropleth(
        locations=df_grouped['state'],
        z=df_grouped['Sentiment_Score'],
        locationmode='USA-states',
        colorscale=color_scale,
        marker_line_color='white'
    ))
    geobar_fig.update_layout(
        title_text='Average Sentiment Score by State',
        geo_scope='usa',
    )

    return fig_pilar, fig_total_yearly, fig_overall, container_style, title_style, heatmap_fig, bubble_fig, boxplot_fig,geobar_fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)


import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output, dash_table

def sentiment_color(score):
    if score <= 50:
        return 'red'
    elif score <= 75:
        return 'yellow'
    else:
        return 'green'

# Load the data
df = pd.read_csv("data/processed_webster.csv")
df['Nuevo_Sentiment_Score'] = df['Smoothed_Sentiment_Score']
df['ds'] = pd.to_datetime(df['ds'])
df1 = df.copy()

# Filter the data to include only records from April 30, 2016, onwards
start_date = '2016-04-30'
df_filtered = df[df['ds'] >= start_date]
df_grouped = df_filtered.groupby(['Bank Name', pd.Grouper(key='ds', freq='M')])['Nuevo_Sentiment_Score'].mean().reset_index()
df_pivot = df_grouped.pivot(index='Bank Name', columns='ds', values='Nuevo_Sentiment_Score')
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

# Create the Dash app layout
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='heatmap', figure=heatmap_fig),
    dash_table.DataTable(id='review-table', columns=[
        {'name': col, 'id': col} for col in df1.columns
    ], page_size=10)
])

@app.callback(
    Output('review-table', 'data'),
    Input('heatmap', 'clickData')
)
def display_reviews(clickData):
    if clickData is None:
        return []
    
    date = clickData['points'][0]['x']
    bank_name = clickData['points'][0]['y']
    
    filtered_df = df1[(df1['ds'].dt.to_period('M') == pd.Period(date, freq='M')) & (df1['Bank Name'] == bank_name)]
    
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

