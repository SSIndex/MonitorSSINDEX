from DashMonitor.app.data.analyzers.base_analyzer import BaseAnalyzer
from DashMonitor.app.handlers.graphics_utils import (
    SENTIMENT_SCORE_GROUPS as gu_SENTIMENT_SCORE_GROUPS,
)
from pandas import Categorical as pd_Categorical, DataFrame as pd_DataFrame


class GeneralComparisonAnalyzer(BaseAnalyzer):
    '''
    GeneralComparisonAnalyzer generates all analysis related to General Tab comparison of the company in its industry.

    Parameters
    ----------
    company_name : str
        Company Name to compare
    industry_name : str
        Industry Name to compare the company with

    Other parameters: args and kwargs are passed to the BaseAnalyzer class
    '''

    def __init__(self, industry_name, company_name, *a, **kw):
        super().__init__(*a, **kw)
        self.__company_name = company_name
        self.__industry_name = industry_name
        self.__data_analyzed = self._BaseAnalyzer__provider()

    def _filter(self):
        '''
        Filter the data analyzed by industry and company name
        '''
        self.__data_industry = self.__data_analyzed[
            self.__data_analyzed['industry'] == self.__industry_name
        ]
        self.__data_company = self.__data_analyzed[
            self.__data_analyzed['bank_name'] == self.__company_name
        ]

    def _group(self): ...

    def _calculate_percentages(self) -> pd_DataFrame:
        """Calculate sentiment category percentage."""
        return (
            self.__data_analyzed["sentiment_category"].value_counts(normalize=True)
            * 100
        )

    def _aggregate(self):
        '''
        Aggregate the data analyzed by sentiment score groups
        '''
        counts_analyzed = self._calculate_percentages()
        counts_industry = self._calculate_percentages()
        counts_company = self._calculate_percentages()

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
                        'Type': self.__industry_name,
                        'Percentage': counts_industry.get(category, 0),
                    },
                    {
                        'Category': category,
                        'Type': self.__company_name,
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
        '''
        Sort the data histogram by category
        '''
        self.__data_histogram.sort_values('Category')

    def execute(self) -> pd_DataFrame:
        '''
        Execute the analyzer filter, group, aggregate, having and sort
        '''
        super().execute()

        return self.__data_histogram
