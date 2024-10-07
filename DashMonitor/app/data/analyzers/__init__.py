'''
Analyzers module. Specific 
'''

from DashMonitor.app.data.analyzers.base_analyzer import BaseAnalyzer
from DashMonitor.app.data.analyzers.general.general_analyzer import (
    GeneralAnalyzer,
)
from DashMonitor.app.data.analyzers.general.general_comparison_analyzer import (
    GeneralComparisonAnalyzer,
)
from DashMonitor.app.data.analyzers.sasb_analyzer import SASBAnalyzer
from DashMonitor.app.data.analyzers.time_trend_analyzer import TimeTrendAnalyzer
