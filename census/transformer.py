# -*- coding: utf-8 -*-
import numpy as np
import yaml
from meta import cols_desc


class ValueMapper(object):
    """class to produce a mapper that sets
    the replacement of the non numeric values to numeric value
    in dataframe"""

    NON_VALIDS_DEFAULT = [' Do not know', ' ?']
    SPECIALS_DEFAULT = [' Not in universe']

    def __init__(self, df,
                 non_valids=NON_VALIDS_DEFAULT,
                 specials=SPECIALS_DEFAULT):
        super(ValueMapper, self).__init__()
        self.df = df
        # values considered as non valid
        self.non_valids = non_valids
        # values considered as specials
        self.specials = specials
        # mapping is a bijective correspondance
        self.mapping = self.__default_mapping()

    # list of columns where the mapper should be build
    def get_string_cols(self):
        col_types = [np.dtype('O')]
        cols = self.df.columns
        return [col for col in cols if self.df[col].dtype in col_types]

    # build mapper that assign to each unique value an integer
    def __default_mapping(self):
        unique_values = {}
        for col in self.get_string_cols():
            unique_values[col] = \
                self.__build_mapping_from_list(self.df[col].unique())
        return unique_values

    # build a dict from the unique values
    def __build_mapping_from_list(self, lst):
        # non valids and special values are treated the same way
        negative_indexed_vals = self.specials + self.non_valids
        j_n = -1  # will be increment on value encounter

        booleans = {' Yes': 1, ' No': 0}

        # value for valid
        j_v = 0

        # TODO buggy when values mix booleans and other valid values
        # keys 0 and 1 will be overriden !
        dct = {}
        for i in range(len(lst)):
            value = lst[i]
            if value in negative_indexed_vals:
                dct[value] = j_n
                j_n -= 1
            elif value in booleans:
                dct[value] = booleans[value]
            else:
                dct[value] = j_v
                j_v += 1
        return dct

    # save map to file
    def to_yamlfile(self, yaml_filepath):
        with open(yaml_filepath, 'w') as outfile:
            outfile.write(yaml.dump(self.mapping, default_flow_style=False))

    # load map from file
    def from_yamlfile(self, yaml_filepath):
        with open(yaml_filepath, 'rt') as infile:
            self.mapping = yaml.load(infile.read())

    # return the df after the mapping has been processed
    def map_result(self):
        new_df = self.df.copy(deep=True)
        for col in self.get_string_cols():
            new_df[col] = new_df[col].map(self.mapping[col])
        return new_df

    # return a string with infos on col and its numerical values
    def get_col_info(self, col):
        # col_meta_infos = [line for line in cols_desc if line[0] == col]
        col_infos = {
            'Code': col,
            'Description': cols_desc[col]
        }
        if col in self.mapping:
            for s, k in self.mapping[col].iteritems():
                col_infos.setdefault(k, [])
                col_infos[k] += [s]
        else:
            col_infos['Type'] = 'numeric'
        return self.__dict_to_string(col_infos)

    def __dict_to_string(self, col_infos):
        s = []
        for k, v in sorted(col_infos.iteritems()):
            s += ["%s : %s" % (str(k), str(v))]
        return "\n".join(s)


if __name__ == '__main__':
    pass
