import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Load the data
df = pd.read_excel("data/df_agrupado_webster_v2.xlsx")
df['year'] = df['ds'].dt.year
df['month'] = df['ds'].dt.month
df = df.groupby(["Bank Name", "Predicted_Pilar", "year", "month"])[["Nuevo_Sentiment_Score"]].mean().reset_index()
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].map('{:02}'.format), format='%Y-%m')
df['Total_Sentiment_Score'] = df.groupby(['Bank Name', 'date'])['Nuevo_Sentiment_Score'].transform('mean')
df.sort_values('date', inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Img(src="/assets/ssindex.png", style={"height": "75px"}),
                width={"size": 2, "offset": 5},
                className="text-center"
            ),
            className="mt-3"
        ),
        dbc.Row(
            dbc.Col(
                html.Button("Cambiar Tema", id="theme-button", className="btn btn-primary", n_clicks=0),
                className="text-end"
            ),
            className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in df['year'].unique()],
                    value=df['year'].max(),
                    clearable=False
                ), width=2),
                dbc.Col(dcc.Dropdown(
                    id='pilar-dropdown',
                    options=[{'label': pilar, 'value': pilar} for pilar in df['Predicted_Pilar'].unique()],
                    value=df['Predicted_Pilar'].unique()[0],
                    clearable=False
                ), width=2),
                dbc.Col(dcc.Checklist(
                    id='bank-checklist',
                    options=[{'label': name, 'value': name} for name in df['Bank Name'].unique()],
                    value=['Webster Bank'],
                    inline=False,
                    style={"display": "flex", "flex-wrap": "wrap", "gap": "10px"}
                ), width=8),
            ],
            className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="main-graph"), width=12),
            ],
            className="mb-3"
        ),
    ],
    fluid=True,
    className="p-3"
)

# Define callback to update the main graph
@app.callback(
    Output("main-graph", "figure"),
    [
        Input("year-dropdown", "value"),
        Input("pilar-dropdown", "value"),
        Input("bank-checklist", "value")
    ]
)
def update_main_graph(selected_year, selected_pilar, selected_banks):
    filtered_df = df[(df['year'] == selected_year) & (df['Predicted_Pilar'] == selected_pilar) & (df['Bank Name'].isin(selected_banks))]
    
    fig_pilar = px.line(filtered_df, x='date', y='Nuevo_Sentiment_Score', color='Bank Name', title=f'Sentiment Score for {selected_year} - {selected_pilar}')
    
    fig_pilar.update_layout(
        plot_bgcolor='white',
        font=dict(family="Roboto"),
        xaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.5)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.5)'),
        paper_bgcolor='white',
        font_color='black'
    )
    
    return fig_pilar

# Define callback to toggle dark mode
@app.callback(
    Output("theme-button", "className"),
    [Input("theme-button", "n_clicks")],
    [dash.dependencies.State("theme-button", "className")]
)
def toggle_theme(n_clicks, current_class):
    if n_clicks % 2 == 1:
        return "btn btn-dark"
    return "btn btn-primary"

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
