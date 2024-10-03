'''
File Stream Provider Class Definition.
'''

# std imports
import re
from typing import List

# # 3rd party imports
from pandas import read_csv as pd_read_csv, to_datetime as pd_to_datetime

# local imports
from DashMonitor.app.data.providers.base_provider import BaseProvider
from DashMonitor.app.handlers.function_utils import categorize_score


class FileStreamProvider(BaseProvider):
    '''
    FileStreamProvider serves data from an file stream as a pandas DataFrame to
    manipulate
    '''

    def __init__(self, path, *a, **kw):
        super().__init__()
        self.path = path
        self.__df = pd_read_csv(path)

        self._clean_columns()
        self._categorize_comments()
        self._generate_year_month_columns()
        self._generate_date_column()

    def __call__(self):
        return self.__df.copy()

    def _clean_columns(self):
        self.__df.columns = [
            re.sub(r'\W+', '_', col.strip().lower()) for col in self.__df.columns
        ]

    def _categorize_comments(self):
        self.__df['sentiment_category'] = self.__df["sentiment_score"].apply(
            categorize_score
        )
        self.__df["normalized_sentiment_score"] = self.__df["sentiment_score"]

    def _generate_date_column(self):
        if "ds" not in set(self.__df.columns):
            self.__df["date"] = pd_to_datetime(
                self.__df["year"].astype(str)
                + "-"
                + self.__df["month_num"].map("{:02}".format),
                format="%Y-%m",
            )
        else:
            self.__df["date"] = self.__df["ds"].astype('datetime64[ns]')

    def _generate_year_month_columns(self):
        if 'year' not in self.__df.columns and 'ds' in self.__df.columns:
            self.__df['year'] = self.__df['ds'].astype('datetime64[ns]').dt.year
        if 'month_num' not in self.__df.columns and 'ds' in self.__df.columns:
            self.__df['month_num'] = self.__df['ds'].astype('datetime64[ns]').dt.month
