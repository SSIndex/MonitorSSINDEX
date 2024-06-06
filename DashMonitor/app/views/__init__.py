'''
Views Package.

Here Layout and html Building will be defined
'''

# std imports

# 3rd party imports
from dash import html

# local imports
from DashMonitor.app.views.configs import (
    EXTERNAL_SCRIPTS,
    EXTERNAL_STYLESHEETS,
    HTML_TITLE,
)

from DashMonitor.app.views.root import MAIN_HTML


ENTRY_LAYOUT = html.Div([])


def setupView(app_settings={}):
    app_settings = dict(
        external_scripts=EXTERNAL_SCRIPTS,
        external_stylesheets=EXTERNAL_STYLESHEETS,
        index_string=MAIN_HTML,
        title=HTML_TITLE,
        **app_settings
    )

    return app_settings
