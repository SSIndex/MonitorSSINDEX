from datetime import date, timedelta

class DateUtils:
    '''Utility class for handling date calculations.'''

    DEFAULT_DATE_RANGES = [0, 5, 30, 91, 182, 365]
    DEFAULT_START_DATE = date.today() - timedelta(days=365)

    def __init__(self, date_ranges=DEFAULT_DATE_RANGES):
        self.date_ranges = date_ranges

    def calculate_start_date_on_index(self, selected_index: int) -> str:
        '''Calculate start date based on self.date_ranges index.'''
        today = date.today()
        if 0 <= selected_index < len(self.date_ranges):
            return today - timedelta(days=self.date_ranges[selected_index])

        # Default start date is 1 year ago if no valid index is provided
        return self.DEFAULT_START_DATE
