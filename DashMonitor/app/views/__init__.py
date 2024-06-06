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
    get_main_html,
    HTML_TITLE,
)


ENTRY_LAYOUT = html.Div([])


def setupView(app_settings={}):
    app_settings = dict(
        external_scripts=EXTERNAL_SCRIPTS,
        external_stylesheets=EXTERNAL_STYLESHEETS,
        index_string=get_main_html(),
        title=HTML_TITLE,
        **app_settings
    )

    return app_settings
