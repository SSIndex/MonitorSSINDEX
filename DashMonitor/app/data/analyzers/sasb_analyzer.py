'''
SASB Analyzer Classes

THIS ANALYZER IS NOT OK, DONT USE YET
'''

from DashMonitor.app.data.analyzers.base_analyzer import BaseAnalyzer


class SASBAnalyzer(BaseAnalyzer):
    '''
    SASBAnalyzer generates all analysis related to General Tab Specifically.
    '''

    def __init__(self, industry_name, company_name, *a, **kw):
        super().__init__(*a, **kw)
        self.__company_name = company_name
        self.__industry_name = industry_name
        self.__data_analyzed = self._BaseAnalyzer__provider()

    def _filter(self):
        df = self.__data_analyzed

        sasb_filter = df["bank_name"] == self.__company_name

        self.__data_analyzed = df[sasb_filter].reset_index(drop=True)

    def _group(self):
        df = self.__data_analyzed

        self.__data_analyzed = (
            df.groupby(["bank_name", "predicted_sasb", "year", "month_num", "date"])[
                ["sentiment_score"]
            ]
            .mean()
            .reset_index()
        )

    def _aggregate(self):
        df = self.__data_analyzed

        df["total_sasb_sentiment_score"] = df.groupby(["predicted_sasb", "date"])[
            "sentiment_score"
        ].transform("mean")

    def _having(self): ...

    def _sort(self):
        self.__data_analyzed.sort_values("date", inplace=True)

    def general_score(self, bank_name):
        df = self.__data_analyzed

        res = df[df["bank_name"] == bank_name]["total_sentiment_score"].mean()

        return 0 if np_isnan(res) else round(res)

    def execute(self):
        super().execute()

        return self.__data_analyzed
