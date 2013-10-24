# -*- coding: utf-8 -*-

# import sys
# sys.path += ['.']
from census.learn import FindBest, most_influential, report_influential, \
    score_report
from census.utils import cols_name_to_indices
from sklearn.linear_model import LogisticRegression
from census.transformer import MyScaler
from sklearn.pipeline import Pipeline
from census.shortcuts import load_datas

# LOAD DATA

limit_to_rows = 199523  # corresponds to the whole dataset
X, y, X_test, y_test, columns, cols_interpret = load_datas(
    nrows=limit_to_rows,
    remove_cols=['YEAR', 'RESI_REGION', 'RESI_PREV', 'RESI_1YEAR',
                 'MIG_REGION', 'MIG_MOVE', 'MIG_MSA', 'INSTANCE_WEIGHT',
                 'ORIG_MOTHER'])


# SET MODEL TYPE IN A PIPELINE

scale_cols = ['AGE', 'INSTANCE_WEIGHT', 'WWORKY', 'WPERH',
              'CAP_GAINS', 'CAP_LOSSES', 'STOCK_DIV']
idx_scale_cols = cols_name_to_indices(columns, scale_cols)
ms = MyScaler(idx_scale_cols)
lr = LogisticRegression(penalty='l1')
predictor = Pipeline([('my_scaling', ms), ('lr', lr)])


# CHECK SCORES WITH RESPECT TO HYPERPARAMETERS

print("CV hyperparameter to be tuned if needed")
tuned_parameters = [
    {'lr__C': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
     'lr__tol': [0.01], 'lr__class_weight': ['auto']}]
fb = FindBest(
    predictor,
    tuned_parameters=tuned_parameters, score='precision', cv=5)

# work on small dataset to tune paramters
limit_to_first_n = 20000
print("For computationnal time, we work with a reduced dataset.")
print("\twe take only the first %s samples." % limit_to_first_n)
bestpl = fb.find(
    X, y, X_test, y_test,
    limit=limit_to_first_n,
    report_results=True, report_classification=True)

# CHOOSE A PREDICTOR AND COMPUTATION

C = 0.1
predictor = Pipeline([
    ('my_scaling', ms),
    ('lr', LogisticRegression(penalty='l1', C=C, tol=0.001))])
# uncomment this, if you want to work with best pipeline
# predictor = bestpl
print("\n\nWE WORK WITH PREDICTOR :")
print(predictor)
print("fit predictor with C=%0.2f\n" % C)
predictor.fit(X, y)

# SCORE ON TEST

score_report(predictor, X_test, y_test)

# PRINT MOST INFLUENTIAL INPUTS AND THEIR COEFS

coefs = predictor.steps[-1][1].coef_[0]
influence = most_influential(coefs, cols_interpret, thres=0.3)
report_influential(influence, nb=20, grouped=False)
report_influential(influence, nb=100, grouped=True)

