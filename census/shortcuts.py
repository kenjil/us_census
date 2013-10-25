# -*- coding: utf-8 -*-
from census.loader import CensusLoader
from census.meta import cols

TARGET = 'TARGET'
TARGET_VALUE_1 = ' 50000+.'
# continuous numerical columns
NUM_COLS_STANDARD = ['AGE', 'INSTANCE_WEIGHT']
NUM_COLS_WITH_ZERO_TREATMENT = \
    ['WWORKY', 'WPERH', 'CAP_GAINS', 'CAP_LOSSES', 'STOCK_DIV']
NUM_COLS = NUM_COLS_STANDARD + NUM_COLS_WITH_ZERO_TREATMENT
# categorical cols
CAT_COLS = [col for col in cols if col not in NUM_COLS + [TARGET]]


# for linear regression
# return data X, y, X_test, y_test, X_cols, X_cols_interpret
def load_datas(dir='data', nrows=None, remove_cols=[], dummify=False):
    print "Loading data from disk..."
    learnds = CensusLoader(dir+'/census_income_learn.csv', cols=cols)
    learndf = learnds.get_data(nrows=nrows)
    testds = CensusLoader(dir+'/census_income_test.csv', cols=cols)
    testdf = testds.get_data(nrows=nrows)

    # TODO could be done in a better way
    # using the read_csv option index_col in census.Loader
    if remove_cols:
        print("Remove columns %r..." % remove_cols)
        cat_cols = [col for col in CAT_COLS if col not in remove_cols]
        # num_cols = [col for col in NUM_COLS if col not in remove_cols]
        learndf = learndf.drop(remove_cols, axis=1)
        testdf = testdf.drop(remove_cols, axis=1)

    print("Transform to dummified, boolean, numerical variables...")

    # dummification, booleans, all numerical variables settings
    from census.transformer import Transformer
    ts = Transformer()
    # create dummy variables from categorical variables
    ts.fit_mapping(learndf, cat_cols=cat_cols)
    ts.fit_dummification(learndf)
    # create a booleans for col with many zeros
    ts.fit_vbools(NUM_COLS_WITH_ZERO_TREATMENT)

    # perform transformation
    n_learndf = ts.transform(learndf.drop([TARGET], axis=1))
    n_testdf = ts.transform(testdf.drop([TARGET], axis=1))

    # get target
    n_learn_target = (learndf[TARGET] == TARGET_VALUE_1).astype(float)
    n_test_target = (testdf[TARGET] == TARGET_VALUE_1).astype(float)

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
