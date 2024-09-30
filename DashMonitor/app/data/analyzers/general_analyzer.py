'''
General Analysis for Dataframe
'''

from DashMonitor.app.data.analyzers.base_analyzer import BaseAnalyzer
from numpy import isnan

class GeneralAnalyzer(BaseAnalyzer):
  '''
  GeneralAnalyzer generates all analysis related to General Tab Specifically.
  '''

  def __init__(self, *a, **kw):
    super().__init__(*a, **kw)
    self.__data_analyzed = self._BaseAnalyzer__provider()


  def _filter_others(self):
    df = self.__data_analyzed
    
    general_filter = (df["Pilar"] == "Other") & (df["Predicted_SASB"] == "Other")

    self.__data_analyzed = df[general_filter].reset_index(drop=True)
  
  
  def _group(self):
    df = self.__data_analyzed

    self.__data_analyzed = (
        df.groupby(["Bank Name", "Predicted_Pilar", "year", "month_num", "date"])[
            ["Sentiment_score"]
        ]
        .mean()
        .reset_index()
    )

  def _agreggate(self):
    df = self.__data_analyzed

    print(f'Columns: {df.columns}')

    df["Total_Sentiment_Score"] = df.groupby(["Bank Name", "date"])[
        "Sentiment_score"
    ].transform("mean")
  
  def _sort(self):
    self.__data_analyzed.sort_values("date", inplace=True)
  
  def general_score(self, bank_name):
    df = self.__data_analyzed

    res = df[df["Bank Name"] == bank_name]["Total_Sentiment_Score"].mean()
    return 0 if isnan(res) else res

  def execute(self):
    self._filter_others()
    self._group()
    self._agreggate()
    self._sort()

    return self.__data_analyzed


class IndustryAnalyzer(BaseAnalyzer):


  def __init__(self, industry_name, *a, **kw):
    super().__init__(*a, **kw)
    self.__data_analyzed = self._BaseAnalyzer__provider()
    self.__data_analyzed = self.__data_analyzed[
      self.__data_analyzed['Industry'] == industry_name
    ]

  def execute(self):
    ...
  ...