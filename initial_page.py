# initial_page.py

import dash
from dash import html, dcc, Input, Output, State
from DashMonitor.app.config import Config
from DashMonitor import main as dash_main
import subprocess
import os
app = dash.Dash(__name__)

# Lista de bancos
bank_options = [
    {"label": "Banco Santander", "value": "Banco Santander"},
    {"label": "Banca Mifel", "value": "Banca Mifel"},
    {"label": "Banco Actinver", "value": "Banco Actinver"},
    {"label": "Banco Azteca", "value": "Banco Azteca"},
    # Agrega aquí los demás bancos
]

# Lista de archivos
file_options = [
    {"label": "Data 1", "value": "/app/DashMonitor/data/data.csv"},
    {"label": "Data 2", "value": "/app/DashMonitor/data/data2.csv"},
]

app.layout = html.Div([
    dcc.Dropdown(
        id='data-path',
        options=file_options,
        placeholder='Select data file'
    ),
    dcc.Dropdown(
        id='bank-name',
        options=bank_options,
        placeholder='Select bank'
    ),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
])

@app.callback(
    Output('output-state', 'children'),
    Input('submit-button', 'n_clicks'),
    State('data-path', 'value'),
    State('bank-name', 'value')
)
def update_output(n_clicks, data_path, bank_name):
    if n_clicks > 0 and data_path and bank_name:
        # Actualiza la configuración global
        Config.data_path = data_path
        Config.bank_name = bank_name
        # Escribir la configuración en un archivo
        with open('/app/config.txt', 'w') as config_file:
            config_file.write(f'data_path={data_path}\n')
            config_file.write(f'bank_name={bank_name}\n')

        with open('/app/start_main_app.signal', 'w') as signal_file:
            signal_file.write('start')
        return f'Data path: {data_path}, Bank name: {bank_name}'
    return ''

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0",  port=8050)
