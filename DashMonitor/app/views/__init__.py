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

from DashMonitor.app.views import components as cpt


ENTRY_LAYOUT = html.Div(
    className='m-0 p-0',
    children=list(
        map(
            lambda x: x.render(),
            (
                cpt.Header(
                    'https://elasticbeanstalk-us-east-1-518344696083.s3.amazonaws.com/esg3-static-files/app/images/Branding2023/03+Isotipo/SVG/4-Negativo+Isotipo.svg',
                    'ESG COMPASS',
                    tabs=[
                        cpt.HeaderTabBtn('general-analysis', 'GENERAL', True),
                        cpt.HeaderTabBtn('sasb-analysis', 'SASB', False),
                        cpt.HeaderTabBtn('ssindex-analysis', 'SSINDEX', False),
                        cpt.HeaderTabBtn('geographic-analysis', 'MAP', False),
                        cpt.HeaderTabBtn('benchmark-analysis', 'BENCHMARK', False),
                    ],
                ),
            ),
        )
    ),
)


def setupView(app_settings={}):
    app_settings = dict(
        external_scripts=EXTERNAL_SCRIPTS,
        external_stylesheets=EXTERNAL_STYLESHEETS,
        index_string=get_main_html(),
        title=HTML_TITLE,
        **app_settings
    )

    return app_settings
