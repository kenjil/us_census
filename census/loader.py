# -*- coding: utf-8 -*-
from pandas import read_csv
from meta import cols_desc


class CensusLoader(object):

    """Loader of Census csv dataset"""
    def __init__(self, csvfile):
        super(CensusLoader, self).__init__()
        self.csvfile = csvfile

    # return a dataframe of predicitives, series of incomes
    def get_data(self):
        whole = read_csv(
            self.csvfile,
            header=None,
            names=self.cols_code
            )
        whole.index.name = 'individual'
        return whole

    @property
    def cols(self):
        return cols_desc

    @property
    def cols_code(self):
        return (cols_desc[i][0] for i in range(len(cols_desc)))

if __name__ == '__main__':
    csloader = CensusLoader('data/census_income_learn.csv')
    # print(csloader.get_data())
    cols = csloader.cols
    print cols
