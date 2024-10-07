'''
Time Trend Analysis for Dataframe
'''

from DashMonitor.app.data.analyzers.base_analyzer import BaseAnalyzer
from numpy import isnan as np_isnan
from pandas import Categorical as pd_Categorical, DataFrame as pd_DataFrame
import pandas as pd


class TimeTrendAnalyzer(BaseAnalyzer):
    '''
    TimeTrendAnalyzer generates all analysis related to Time Trend Tab Specifically.
    '''

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.__data_analyzed = self._BaseAnalyzer__provider()

    def _filter(self):
        pass

    def _group(self):
        '''
        Group the data analyzed by company name, predicted pilar, year, month number and date
        and calculate the mean of the sentiment score
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
        Aggregate the data analyzed by company name and date and calculate the mean of the sentiment score
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

    def _transform(self):
        '''
        Transform the data analyzed by adding a date column with the year and month number
        '''
        df = self.__data_analyzed
        self.__data_analyzed["date"] = pd.to_datetime(
            df["year"].astype(str) + "-" + df["month_num"].map("{:02}".format),
            format="%Y-%m",
        )

    def size(self) -> tuple:
        '''
        Return the size of the data analyzed
        '''
        return self.__data_analyzed.shape

    def general_score(self, bank_name: str) -> int:
        '''
        Calculate the general score for a company
        '''
        df = self.__data_analyzed

        res = df[df["bank_name"] == bank_name]["total_sentiment_score"].mean()

        return 0 if np_isnan(res) else round(res)

    def get_all_reviews_by_company(self, bank_name : str) -> pd_DataFrame:
        '''
        Get all the data analyzed for a company
        '''
        df = self.__data_analyzed

        return df[df["bank_name"] == bank_name]

    def execute(self) -> pd_DataFrame:
        '''
        Execute the analyzer filter, group, aggregate, having and sort
        '''
        super().execute()

        return self.__data_analyzed
