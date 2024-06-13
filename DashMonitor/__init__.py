'''
DashMonitor Package.

This file will encapsulate the setup of the Dash server
'''

# std imports

# 3rd party imports

# local imports
from DashMonitor.app import app


def main():
    '''
    Main function to setup and config the execution of the app
    '''
    print(f'Hello from {__name__}')

    app.run_server(debug=True, host="0.0.0.0", port=8052)
