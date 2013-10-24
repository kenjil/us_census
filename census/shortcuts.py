# -*- coding: utf-8 -*-
from census.loader import CensusLoader
from census.meta import cols


# return data X, y, X_test, y_test, X_cols, X_cols_interpret
def load_datas(dir='data', nrows=None, remove_cols=[]):
    print "Loading data from disk..."
    learnds = CensusLoader(dir+'/census_income_learn.csv', cols=cols)
    learndf = learnds.get_data(nrows=nrows)
    testds = CensusLoader(dir+'/census_income_test.csv', cols=cols)
    testdf = testds.get_data(nrows=nrows)

    target = ['TARGET']
    # continuous numerical columns
    num_cols_standard = ['AGE', 'INSTANCE_WEIGHT']
    num_cols_with_zero_treatment = \
        ['WWORKY', 'WPERH', 'CAP_GAINS', 'CAP_LOSSES', 'STOCK_DIV']
    num_cols = num_cols_standard + num_cols_with_zero_treatment
    # categorical cols
    cat_cols = [col for col in cols if col not in num_cols + target]

    # TODO could be done in a better way
    # using the read_csv option index_col in census.Loader
    if remove_cols:
        print("Remove columns %r..." % remove_cols)
        cat_cols = [col for col in cat_cols if col not in remove_cols]
        num_cols = [col for col in num_cols if col not in remove_cols]
        learndf = learndf.drop(remove_cols, axis=1)
        testdf = testdf.drop(remove_cols, axis=1)

    print("Transform to dummified, boolean, numerical variables...")

    # dummification, booleans, all numerical variables settings
    from census.transformer import Transformer
    ts = Transformer()
    # create dummy variables from categorical variables
    ts.fit_dummification(learndf, cat_cols=cat_cols)
    # create a booleans for col with many zeros
    ts.fit_vbools(num_cols_with_zero_treatment)

    # perform transformation
    n_learndf = ts.transform(learndf.drop(['TARGET'], axis=1))
    n_testdf = ts.transform(testdf.drop(['TARGET'], axis=1))

    # get target
    n_learn_target = (learndf['TARGET'] == ' 50000+.').astype(float)
    n_test_target = (testdf['TARGET'] == ' 50000+.').astype(float)

    # get human understandable col names of transformed df
    cols_interprets = [
        ts.interpret_dummy_col_name(col) for col in n_learndf]

    print("Convert data to np.array and return")
    print("\tX, y, X_test, y_test, X_cols_name, X_cols_interprets...")

    # work with np.array
    X = n_learndf.as_matrix()
    X_test = n_testdf.as_matrix()
    y = n_learn_target.tolist()
    y_test = n_test_target.tolist()

    return X, y, X_test, y_test, n_learndf.columns.tolist(), cols_interprets
