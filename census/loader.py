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
            names=self.cols_code
            )
        whole.index.name = 'individual'
        return whole

    @property
    def cols_code(self):
        return (self.cols[i][0] for i in range(len(self.cols)))

if __name__ == '__main__':
    csloader = CensusLoader('data/census_income_learn.csv')
    # print(csloader.get_data())
    cols = csloader.cols
    print cols
