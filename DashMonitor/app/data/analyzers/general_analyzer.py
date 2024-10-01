'''
General Analysis for Dataframe
'''

from DashMonitor.app.data.analyzers.base_analyzer import BaseAnalyzer
from DashMonitor.app.handlers.graphics_utils import (
    CATEGORY_ORDER as gu_CATEGORY_ORDER,
    SENTIMENT_SCORE_GROUPS as gu_SENTIMENT_SCORE_GROUPS,
)
from numpy import isnan as np_isnan
from pandas import Categorical as pd_Categorical, DataFrame as pd_DataFrame


class GeneralAnalyzer(BaseAnalyzer):
    '''
    GeneralAnalyzer generates all analysis related to General Tab Specifically.
    '''

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.__data_analyzed = self._BaseAnalyzer__provider()

    def _filter(self):
        df = self.__data_analyzed

        general_filter = (df["pilar"] == "Other") & (df["predicted_sasb"] == "Other")

        self.__data_analyzed = df[general_filter].reset_index(drop=True)

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

    def general_score(self, bank_name):
        df = self.__data_analyzed

        res = df[df["bank_name"] == bank_name]["total_sentiment_score"].mean()
        return 0 if np_isnan(res) else res

    def execute(self):
        super().execute()

        return self.__data_analyzed


class GeneralComparisonAnalyzer(BaseAnalyzer):

    def __init__(self, industry_name, company_name, *a, **kw):
        super().__init__(*a, **kw)
        self.__company_name = company_name
        self.__industry_name = industry_name
        self.__data_analyzed = self._BaseAnalyzer__provider()

    def _filter(self):
        self.__data_industry = self.__data_analyzed[
            self.__data_analyzed['industry'] == self.__industry_name
        ]
        self.__data_company = self.__data_analyzed[
            self.__data_analyzed['bank_name'] == self.__company_name
        ]

    def _group(self): ...

    def _aggregate(self):
        counts_analyzed = (
            self.__data_analyzed["sentiment_category"].value_counts(normalize=True)
            * 100
        )
        counts_industry = (
            self.__data_industry["sentiment_category"].value_counts(normalize=True)
            * 100
        )
        counts_company = (
            self.__data_company["sentiment_category"].value_counts(normalize=True) * 100
        )

        df = pd_DataFrame(
            [
                category_counts
                for category in gu_SENTIMENT_SCORE_GROUPS
                for category_counts in (
                    {
                        'Category': category,
                        'Type': 'Universe',
                        'Percentage': counts_analyzed.get(category, 0),
                    },
                    {
                        'Category': category,
                        'Type': 'Industry',
                        'Percentage': counts_industry.get(category, 0),
                    },
                    {
                        'Category': category,
                        'Type': 'Company',
                        'Percentage': counts_company.get(category, 0),
                    },
                )
            ]
        )

        df['Category'] = pd_Categorical(
            df['Category'], categories=gu_SENTIMENT_SCORE_GROUPS, ordered=True
        )

        self.__data_histogram = df

    def _having(self): ...

    def _sort(self):
        self.__data_histogram.sort_values('Category')

    def execute(self):
        super().execute()

        return self.__data_histogram

    ...
