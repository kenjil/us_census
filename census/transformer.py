# -*- coding: utf-8 -*-
import numpy as np
import yaml
from meta import cols_desc
from stats import BasicStatistic
from sklearn.preprocessing import OneHotEncoder
from pandas import DataFrame, concat


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
        # mapping
        self.mapping = {}

    # list of columns where the mapper should be build
    def get_string_cols(self):
        col_types = [np.dtype('O')]
        cols = self.df.columns
        return [col for col in cols if self.df[col].dtype in col_types]

    # build mapper that assign to each unique value an integer
    def build_default_mapping(self, sort=False, cols_list=None):
        if cols_list is None:
            cols_list = self.get_string_cols()
        for col in cols_list:
            self.build_default_col_mapping(col, sort=sort)
            # unique_values[col] = \
            #     self.__build_mapping_from_list(self.df[col].unique())
        # self.mapping = unique_values

    def build_default_col_mapping(self, col, sort=False):
        if sort is True:
            bs = BasicStatistic(self.df,
                                non_valids=self.non_valids,
                                specials=self.specials,
                                cols_desc={})
            target_value_sort = ' 50000+.'
            sort_index = bs.percentage(bs.count_values_per_target(col))[target_value_sort]
            sort_index = sort_index.copy()
            sort_index.sort()
            self.build_col_mapping(col, sort_index.index)
        else:
            self.build_col_mapping(col, self.df[col].unique())

    def build_col_mapping(self, col, lst):
        self.mapping[col] = self.__build_mapping_from_list(lst)

    # build a dict from the unique values
    def __build_mapping_from_list(self, lst):
        # non valids and special values are treated the same way
        last_vals = self.specials + self.non_valids
        last_vals = [i for i in lst if i in last_vals]
        j_n = len(lst) - 1  # will be increment negatively on value encounter

        booleans = {' Yes': 1, ' No': 0}

        # value for valid
        j_v = 0

        # TODO buggy when values mix booleans and other valid values
        # keys 0 and 1 will be overriden !
        dct = {}
        for i in range(len(lst)):
            value = lst[i]
            if value in last_vals:
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
    def map_result(self, df):
        new_df = df.copy(deep=True)
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


class Preprocess(object):
    """docstring for Preprocess"""
    def __init__(self, learndf, settings={}):
        super(Preprocess, self).__init__()
        self.learndf = learndf
        self.settings = settings
        self.mapper = None
        # puts in memory to speed up run
        self.__mapper_enc = None
        self.__mapper_dummy_cols_name = None

    # categorical cols list define in mapper
    @property
    def cat_cols(self):
        if self.mapper:
            return self.mapper.mapping.keys()
        else:
            return []

    # set the mapper for categorical preprocessing
    def set_mapper(self,
                   non_valids=[],
                   specials=[],
                   cat_cols=[]):
        self.mapper = ValueMapper(self.learndf,
                                  non_valids=non_valids,
                                  specials=specials)
        self.mapper.build_default_mapping(sort=True, cols_list=cat_cols)
        self.set_mapper_enc()
        self.set_mapper_dummy_cols_name()

    # OneHotEncoder implicitely defined by mapper
    def set_mapper_enc(self):
        enc = OneHotEncoder()
        n_learndf = self.mapper.map_result(self.learndf)
        enc.fit(n_learndf[self.cat_cols])
        self.__mapper_enc = enc

    # cols name of the dummy variables
    # by self.produced get_OneHotEncoder
    def set_mapper_dummy_cols_name(self):
        cols_name = []
        for col in self.cat_cols:
            for j in range(len(self.mapper.mapping[col])):
                cols_name += [col+'__%d' % j]
        self.__mapper_dummy_cols_name = cols_name

    def run(self, df):
        new_df = df.copy()
        dummys_df = self.get_dummys(df)
        return concat([new_df, dummys_df], axis=1)

    def get_dummys(self, df):
        if self.mapper:
            new_df = self.mapper.map_result(df)
            enc = self.__mapper_enc
            cols_name = self.__mapper_dummy_cols_name
            data_ar = enc.transform(new_df[self.cat_cols]).toarray()
            return DataFrame(data_ar, columns=cols_name)
        else:
            return None



if __name__ == '__main__':
    pass
