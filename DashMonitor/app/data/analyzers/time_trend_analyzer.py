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
        df = self.__data_analyzed

        self.__data_analyzed = (
            df.groupby(["bank_name", "predicted_pilar", "year", "month_num", "date"])[
                ["sentiment_score"]
            ]
            .mean()
            .reset_index()
        )

    def _aggregate(self):
        df = self.__data_analyzed

        df["total_sentiment_score"] = df.groupby(["bank_name", "date"])[
            "sentiment_score"
        ].transform("mean")

    def _having(self): ...

    def _sort(self):
        self.__data_analyzed.sort_values("date", inplace=True)

    def _transform(self):
        df = self.__data_analyzed
        self.__data_analyzed["date"] = pd.to_datetime(
            df["year"].astype(str) + "-" + df["month_num"].map("{:02}".format),
            format="%Y-%m",
        )

    def size(self) -> tuple:
        return (self.__data_analyzed.shape[0], self.__data_analyzed.shape[1])

    def general_score(self, bank_name):
        df = self.__data_analyzed

        res = df[df["bank_name"] == bank_name]["total_sentiment_score"].mean()

        return 0 if np_isnan(res) else round(res)

    def get_all_reviews_by_company(self, bank_name):
        df = self.__data_analyzed

        return df[df["bank_name"] == bank_name]

    def execute(self):
        super().execute()

        return self.__data_analyzed
