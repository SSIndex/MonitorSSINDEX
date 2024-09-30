'''
Configs module with all view related configurations and constants.
'''

# local imports
from DashMonitor.app.data.providers import FileStreamProvider

HTML_TITLE = 'ESG COMPASS'

EXTERNAL_STYLESHEETS = []

EXTERNAL_SCRIPTS = [
    {'src': 'https://code.jquery.com/jquery-3.6.0.min.js'},
    {
        'src': 'https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js'
    },
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js'
    },
]

main_df_provider = FileStreamProvider(
    '/app/DashMonitor/data/boeing_case_use.csv'
)


def get_main_html() -> str:
    with open('DashMonitor/app/views/main.html', 'r') as main_html_buffer:
        return main_html_buffer.read()
