'''
DashMonitor Package.

This file will encapsulate the setup of the Dash server
'''
# std imports

# 3rd party imports

# local imports
from DashMonitor.app.data import *
from DashMonitor.app.handlers import *
from DashMonitor.app.views import *

# import dash
# from dash import Dash, html, dcc, Input, Output, State, dash_table
# import dash_bootstrap_components as dbc
# import plotly.express as px
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go

def main():
    print(f'Hello from {__name__}')

    app.run_server(debug=True, host="0.0.0.0", port=8052)

if __name__ == "__main__":
    ...