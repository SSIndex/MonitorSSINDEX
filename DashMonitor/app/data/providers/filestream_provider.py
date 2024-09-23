'''
File Stream Provider Class Definition.
'''

# std imports
from typing import List

# # 3rd party imports
from pandas import read_csv as pd_read_csv

# local imports
from DashMonitor.app.data.providers.base_provider import BaseProvider


class FileStreamProvider(BaseProvider):
    '''
    FileStreamProvider serves data from an file stream as a pandas DataFrame to
    manipulate
    '''

    def __init__(self, path, *a, **kw):
        super().__init__()
        self.path = path
        self.__df = pd_read_csv(path)

    def __call__(self):
        return self.__df
