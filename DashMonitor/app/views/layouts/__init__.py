'''
Layouts Module. All Layouts will be added here
'''

from DashMonitor.app.views.layouts.benchmark_analysis import (
    BENCHMARK_ANALYSIS_LAYOUT,
    register_layout_and_callbacks_benchmark,
)
from DashMonitor.app.views.layouts.general_analysis import GENERAL_ANALYSIS_LAYOUT
from DashMonitor.app.views.layouts.geographic_analysis import (
    GEOGRAPHIC_ANALYSIS_LAYOUT,
    register_layout_and_callbacks_map,
)
from DashMonitor.app.views.layouts.sasb_analysis import (
    SASB_ANALYSIS_LAYOUT,
    register_layout_and_callbacks_sasb,
)
from DashMonitor.app.views.layouts.ssindex_analysis import (
    SSINDEX_ANALYSIS_LAYOUT,
    register_layout_and_callbacks_ssindex,
)


def register_layouts_and_callbacks(app):
    register_layout_and_callbacks_benchmark(app)
    register_layout_and_callbacks_map(app)
    register_layout_and_callbacks_sasb(app)
    # register_layout_and_callbacks_ssindex(app)

    return app
