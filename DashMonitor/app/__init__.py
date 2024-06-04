'''
App Package.

All App configurations will be declared here.
'''
# std imports

# 3rd party imports
from dash import Dash

# local imports
import DashMonitor.app.data as data
import DashMonitor.app.handlers as handlers
from DashMonitor.app.views import (
    ENTRY_LAYOUT as view_layout,
    setupView
)


view_settings = setupView({})

app = Dash(__name__, **view_settings)
app.layout = view_layout
