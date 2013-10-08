# -*- coding: utf-8 -*-
import numpy as np
import yaml


class ValueMapper(object):
    """class to produce a mapper that sets
    the replacement of the non numeric values to numeric value
    in dataframe"""
    def __init__(self, df):
        super(ValueMapper, self).__init__()
        self.df = df
        self.mapping = self.default_mapper()

    # list of columns where the mapper should be build
    def get_string_cols(self):
        col_types = [np.dtype('O')]
        cols = self.df.columns
        return [col for col in cols if self.df[col].dtype in col_types]

    # build mapper that assign to each unique value an integer
    def default_mapper(self):
        unique_values = {}
        for col in self.get_string_cols():
            unique_values[col] = \
                self.__build_mapper_from_list(self.df[col].unique())
        return unique_values

    # build a dict from the unique values
    def __build_mapper_from_list(self, lst):
        # numeric value for non_valid
        non_valids = (' Not in universe', ' Do not know', ' ?')
        j_n = -1  # will be increment on value encounter

        booleans = {' Yes': 1, ' No': 0}

        # value for valid
        j_v = 0

        # TODO buggy when value mix booleans and other valid values
        # keys 0 and 1 will be overriden !
        dct = {}
        for i in range(len(lst)):
            if lst[i] in non_valids:
                dct[j_n] = lst[i]
                j_n -= 1
            elif lst[i] in booleans:
                dct[booleans[lst[i]]] = lst[i]
            else:
                dct[j_v] = lst[i]
                j_v += 1
        return dct

    # save map to file
    def to_yaml(self, yaml_filepath):
        with open(yaml_filepath, 'w') as outfile:
            outfile.write(yaml.dump(self.mapping, default_flow_style=False))

    # load map from file
    def from_yaml(self, yaml_filepath):
        with open(yaml_filepath, 'rt') as infile:
            self.mapping = yaml.load(infile.read())




if __name__ == '__main__':
    pass
