# -*- coding: utf-8 -*-
from pandas import read_csv


class CensusLoader(object):
    """Loader of Census csv dataset"""
    # csvfile : csv pathfile
    # cols : tuple of pairs (col_code, col_description)
    def __init__(self, csvfile, cols=()):
        super(CensusLoader, self).__init__()
        self.csvfile = csvfile
        self.cols = cols

    # return a dataframe containing census data
    def get_data(self):
        whole = read_csv(
            self.csvfile,
            header=None,
            names=self.cols
            )
        whole.index.name = 'individual'
        return whole

if __name__ == '__main__':
    pass
