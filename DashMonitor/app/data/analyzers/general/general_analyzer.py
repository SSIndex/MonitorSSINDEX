'''
General Analysis for Dataframe
'''

from DashMonitor.app.data.analyzers.base_analyzer import BaseAnalyzer
from numpy import isnan as np_isnan
from pandas import DataFrame as pd_DataFrame


class GeneralAnalyzer(BaseAnalyzer):
    '''
    GeneralAnalyzer generates all analysis related to General Tab Specifically.
    '''

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.__data_analyzed = self._BaseAnalyzer__provider()

    def _filter(self):
        '''
        Filter the data analyzed
        '''
        df = self.__data_analyzed

        general_filter = (df["pilar"] != "Other") & (df["predicted_sasb"] != "Other")

        self.__data_analyzed = df[general_filter].reset_index(drop=True)

    def _group(self):
        '''
        Group the data analyzed by company name, predicted pilar, year, month number and date
        '''
        df = self.__data_analyzed

        self.__data_analyzed = (
            df.groupby(["bank_name", "predicted_pilar", "year", "month_num", "date"])[
                ["sentiment_score"]
            ]
            .mean()
            .reset_index()
        )

    def _aggregate(self):
        '''
        Aggregate the data analyzed by company name and date
        '''
        df = self.__data_analyzed

        df["total_sentiment_score"] = df.groupby(["bank_name", "date"])[
            "sentiment_score"
        ].transform("mean")

    def _having(self): ...

    def _sort(self):
        '''
        Sort the data analyzed by date
        '''
        self.__data_analyzed.sort_values("date", inplace=True)

    def size(self) -> tuple:
        '''
        Return the size of the analyzed
        '''
        return self.__data_analyzed.shape

    def general_score(self, bank_name) -> int:
        '''
        Calculate the general score for a company
        '''
        df = self.__data_analyzed

        res = df[df["bank_name"] == bank_name]["total_sentiment_score"].mean()

        return 0 if np_isnan(res) else round(res)

    def execute(self) -> pd_DataFrame:
        '''
        Execute the analyzer filter, group, aggregate, having and sort
        '''
        super().execute()

        return self.__data_analyzed
