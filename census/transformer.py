# -*- coding: utf-8 -*-
import numpy as np
import yaml


class ValueMapper(object):
    """class to produce a mapper that sets
    the replacement of the non numeric values to numeric value
    in dataframe"""

    NON_VALIDS_DEFAULT = [' Not in universe', ' Do not know', ' ?']

    def __init__(self, df, non_valids=NON_VALIDS_DEFAULT):
        super(ValueMapper, self).__init__()
        self.df = df
        # values considered as non valid
        self.non_valids = non_valids
        # mapping is a bijective correspondance
        self.mapping = self.default_mapping()

    # list of columns where the mapper should be build
    def get_string_cols(self):
        col_types = [np.dtype('O')]
        cols = self.df.columns
        return [col for col in cols if self.df[col].dtype in col_types]

    # build mapper that assign to each unique value an integer
    def default_mapping(self):
        unique_values = {}
        for col in self.get_string_cols():
            unique_values[col] = \
                self.__build_mapping_from_list(self.df[col].unique())
        return unique_values

    # build a dict from the unique values
    def __build_mapping_from_list(self, lst):
        # numeric value for non_valid
        # non valids values are in self.non_valids
        j_n = -1  # will be increment on value encounter

        booleans = {' Yes': 1, ' No': 0}

        # value for valid
        j_v = 0

        # TODO buggy when values mix booleans and other valid values
        # keys 0 and 1 will be overriden !
        dct = {}
        for i in range(len(lst)):
            value = lst[i]
            if value in self.non_valids:
                dct[value] = j_n
                j_n -= 1
            elif value in booleans:
                dct[value] = booleans[value]
            else:
                dct[value] = j_v
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

    # return the df after the mapping has been processed
    def map_result(self):
        new_df = self.df.copy(deep=True)
        for col in self.get_string_cols():
            new_df[col] = new_df[col].map(self.mapping[col])
        return new_df


if __name__ == '__main__':
    pass
