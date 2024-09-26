'''
Views Package.

Here Layout and html Building will be defined
'''

# std imports

# 3rd party imports
from dash.html import Div
from dash.dcc import Store

# local imports
from DashMonitor.app.views.configs import (
    EXTERNAL_SCRIPTS,
    EXTERNAL_STYLESHEETS,
    get_main_html,
    HTML_TITLE,
)

from DashMonitor.app.views import components as cpt
from DashMonitor.app.views import layouts as lyt

GLOBAL_STATE = [
    Store(id='stateCompanyName', data={}, storage_type='local'),
    Store(id='stateMainDataFrame', data={}),
]


ENTRY_LAYOUT = Div(
    className='m-0 p-0',
    children=[
        *GLOBAL_STATE,
        *list(
            map(
                lambda x: x.render(),
                (
                    cpt.Header(
                        'https://elasticbeanstalk-us-east-1-518344696083.s3.amazonaws.com/esg3-static-files/app/images/Branding2023/03+Isotipo/SVG/4-Negativo+Isotipo.svg',
                        'ESG COMPASS',
                        tabs=[
                            cpt.HeaderTabBtn('GENERAL'),
                            cpt.HeaderTabBtn('SASB'),
                            cpt.HeaderTabBtn('SSINDEX'),
                            cpt.HeaderTabBtn('MAP'),
                            cpt.HeaderTabBtn('BENCHMARK'),
                        ],
                    ),
                    cpt.Main(
                        tab_bodies=[
                            cpt.MainTabPanel(
                                'GENERAL', view=lyt.GENERAL_ANALYSIS_LAYOUT
                            ),
                            cpt.MainTabPanel('SASB', view=lyt.SASB_ANALYSIS_LAYOUT),
                            cpt.MainTabPanel(
                                'SSINDEX', view=lyt.SSINDEX_ANALYSIS_LAYOUT
                            ),
                            cpt.MainTabPanel(
                                'MAP', view=lyt.GEOGRAPHIC_ANALYSIS_LAYOUT
                            ),
                            cpt.MainTabPanel(
                                'BENCHMARK', view=lyt.BENCHMARK_ANALYSIS_LAYOUT
                            ),
                        ]
                    ),
                    cpt.Footer(),
                ),
            )
        ),
    ],
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


def register_views_layouts(app):
    return lyt.register_layouts_and_callbacks(app)
