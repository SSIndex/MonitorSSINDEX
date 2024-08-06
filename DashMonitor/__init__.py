'''
DashMonitor Package.

This file will encapsulate the setup of the Dash server
'''

# std imports

# 3rd party imports

# local imports
from DashMonitor.app import app
from DashMonitor.app.config import Config 
from DashMonitor.app.views.layouts.sasb_analysis import register_layout_and_callbacks_sasb
from DashMonitor.app.views.layouts.ssindex_analysis import register_layout_and_callbacks_ssindex
from DashMonitor.app.views.layouts.geographic_analysis import register_layout_and_callbacks_map
from DashMonitor.app.views.layouts.benchmark_analysis import register_layout_and_callbacks_benchmark

def main():
    '''
    Main function to setup and config the execution of the app
    '''
    register_layout_and_callbacks_sasb(app)
    register_layout_and_callbacks_ssindex(app)
    register_layout_and_callbacks_map(app)
    register_layout_and_callbacks_benchmark(app)

    print(f'Hello from {__name__}')

    app.run_server(debug=True, host="0.0.0.0", port=8052)
