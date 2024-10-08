'''
Map Analysys for Dataframe
'''

from DashMonitor.app.data.analyzers.base_analyzer import BaseAnalyzer


class MapAnalyzer(BaseAnalyzer):
    '''
    MapAnalyzer generates all analysis related to Map Tab Specifically.
    '''

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.__data_analyzed = self._BaseAnalyzer__provider()

    def _filter(self):
        pass

    def _group(self):
        df = self.__data_analyzed

        self.__data_analyzed = (
            df.groupby(["bank_name", "state"])[["sentiment_score"]].mean().reset_index()
        )

    def _aggregate(self): ...

    def _having(self): ...

    def _sort(self): ...

    def get_all_reviews_by_company(self, bank_name):
        df = self.__data_analyzed

        return df[df["bank_name"] == bank_name]

    def execute(self):
        super().execute()
        return self.__data_analyzed
