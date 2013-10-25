# -*- coding: utf-8 -*-
from stats import BasicStatistic
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from pandas import DataFrame, concat, Series
from sklearn.base import BaseEstimator, TransformerMixin


class LabelMapper(object):
    """class to produce a mapper that sets
    the replacement of the non numeric values to numeric value
    in dataframe"""

    def __init__(self):
        super(LabelMapper, self).__init__()
        # mapping
        self.mapping = {}

    # build mapper that assign to each unique value an integer
    # when df is a series, cat_cols can be omitted
    # when df is a DataFrame, cat_cols is the list of categorical columns
    def fit(self, df, cat_cols=None, sort_col_df=None, sort_value=None):
        # if df is a pandas Series
        if cat_cols is None:
            self.build_default_col_mapping(
                df, sort_col_df=sort_col_df, sort_value=sort_value)
        # if df is a pandas DataFrame
        else:
            for col in cat_cols:
                self.build_default_col_mapping(
                    df[col], sort_col_df=sort_col_df, sort_value=sort_value)

    # build mapper for a columns
    def build_default_col_mapping(
            self, col_df,
            sort_col_df=None, sort_value=None):
        if sort_col_df is not None:
            bs = BasicStatistic()
            t = bs.count_values_per_target(col_df, sort_col_df)
            sort_index = \
                bs.percentage(t)[sort_value]
            sort_index = sort_index.copy()
            sort_index.sort()
            self.build_col_mapping(col_df.name, list(sort_index.index))
        else:
            self.build_col_mapping(col_df.name, col_df.unique())

    def build_col_mapping(self, col_name, lst):
        le = LabelEncoder()
        le.fit(lst)
        self.mapping[col_name] = le

    # return the df after the mapping has been processed
    def map_result(self, df):
        new_df = df.copy(deep=True)
        if type(df) == Series:
            return self.mapping[df.name].transform(df)
        else:
            cols = [col for col in self.mapping if col in df.columns]
            for col in cols:
                new_df[col] = self.mapping[col].transform(new_df[col])
            return new_df


class Transformer(object):
    """Transformer is the class to produce for a raw census DataFrame
    a new DataFrame with :
    - new boolean predictive variables
    - set the numerical replacement of categorical label
    - dummy coding varibles

    The transformer is fitted with on the learndf dataset
    with Transformer.fit(learndf)

    The new dataframe produced by Transformer.transform(df) is equivalent
    to df in term of data information
    """
    def __init__(self):
        super(Transformer, self).__init__()
        self.mapper = None
        self.vbools = {}
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

    # binarized cols list define in binarizer
    @property
    def vbool_cols(self):
        if self.vbools:
            return self.vbools.keys()
        else:
            return []

    # set the mapper for categorical inputs
    def fit_mapping(
            self, learndf,
            cat_cols=None,
            sort_col_df=None,
            sort_value=None
            ):
        self.mapper = LabelMapper()
        self.mapper.fit(
            learndf,
            cat_cols=cat_cols,
            sort_col_df=sort_col_df,
            sort_value=sort_value)

    # set the mapper for categorical preprocessing
    def fit_dummification(self, learndf):
        if self.mapper is None:
            # TODO should raise some error
            print "No mapper has been fit => dummification error"
        self.set_mapper_enc(learndf)
        self.set_mapper_dummy_cols_name()

    # set the list of boolean variables that must be derived
    # if vbool_vals is None, boolean variables will be of the
    # form : value == 0
    #  vbool_cols: list of columns name
    #  vbool_vals: list of columns value to check against
    def fit_vbools(
            self,
            vbool_cols,
            vbool_vals=None):
        if vbool_vals is None:
            for col in vbool_cols:
                self.vbools[col] = 0
        else:
            for i in range(len(vbool_cols)):
                self.vbools[vbool_cols[i]] = vbool_vals[i]

    # OneHotEncoder implicitely defined by mapper
    def set_mapper_enc(self, learndf):
        enc = OneHotEncoder()
        n_learndf = self.mapper.map_result(learndf)
        enc.fit(n_learndf[self.cat_cols])
        self.__mapper_enc = enc

    # cols name of the dummy variables
    # by self.produced get_OneHotEncoder
    def set_mapper_dummy_cols_name(self):
        cols_name = []
        for col in self.cat_cols:
            for j in range(len(self.mapper.mapping[col].classes_)):
                cols_name += [col+'__%d' % j]
        self.__mapper_dummy_cols_name = cols_name

    # transform df to get dummified and booleans variables
    def transform(self, df):
        new_df = df.copy()
        new_df = self.mapper.map_result(new_df)
        dummys_df = self.get_dummys(new_df)
        bools_df = self.get_booleans(new_df)
        return concat(
            [new_df.drop(self.cat_cols, 1), bools_df, dummys_df],
            axis=1)

    # return the df with the dummy variables
    def get_dummys(self, df):
        if self.__mapper_enc is not None:
            enc = self.__mapper_enc
            cols_name = self.__mapper_dummy_cols_name
            data_ar = enc.transform(df[self.cat_cols]).toarray()
            return DataFrame(data_ar, columns=cols_name)
        else:
            return None

    # return the df with the boolean variables
    def get_booleans(self, df):
        if self.vbools:
            vbools_df_stack = []
            for col in self.vbools:
                serie = (df[col] == self.vbools[col]).astype(int)
                serie.name = "%s_eq_%d" % (col, self.vbools[col])
                vbools_df_stack += [serie]
        return concat(vbools_df_stack, axis=1)

    # retrieve a string to interpret dummy variables from their name
    def interpret_dummy_col_name(self, string):
        if string.find('__') != -1:
            col, num_val = string.split('__')
            num_val = int(num_val)
            labelenc = self.mapper.mapping[col]
            return "%s = %s" % (col, labelenc.inverse_transform(num_val))
        return "%s columns" % string


class MyScaler(BaseEstimator, TransformerMixin):
    """MyScaler scales a subset of the columns"""
    def __init__(self, num_cols):
        super(MyScaler, self).__init__()
        self.num_cols = num_cols
        self.ss = StandardScaler()

    def fit(self, X, y=None):
        self.ss.fit(X[:, self.num_cols])
        return self

    def transform(self, X, y=None):
        X[:, self.num_cols] = self.ss.transform(X[:, self.num_cols])
        return X

if __name__ == '__main__':
    pass
