# -*- coding: utf-8 -*-

# import sys
# sys.path += ['.']
from census.learn import FindBest, most_influential, report_influential, \
    score_report
from census.utils import cols_name_to_indices
from sklearn.ensemble import RandomForestClassifier
from census.transformer import MyScaler
from sklearn.pipeline import Pipeline
from census.shortcuts import load_datas

print("""
Loading data from disk and transform it with :
  - categorical variables are label so that the corresponding
  numerical values are growing with the proportion of +50.000$
""")

limit_to_rows = 199523  # corresponds to the whole dataset
X, y, X_test, y_test, columns, cols_interpret = load_datas(
    nrows=limit_to_rows,
    sort_mapping=True,
    booleans=False
    # dummify=True
    )

# SET MODEL TYPE IN A PIPELINE

scale_cols = ['AGE', 'INSTANCE_WEIGHT', 'WWORKY', 'WPERH',
              'CAP_GAINS', 'CAP_LOSSES', 'STOCK_DIV']
idx_scale_cols = cols_name_to_indices(columns, scale_cols)
ms = MyScaler(idx_scale_cols)
rf = RandomForestClassifier(n_jobs=-1)
predictor = Pipeline([('my_scaling', ms), ('rf', rf)])


print("""
---------------------------------
TUNING OF HYPERPARAMETERS EXAMPLE
---------------------------------
must be ran on many more samples to be really valuable.
""")

# CHECK SCORES WITH RESPECT TO HYPERPARAMETERS

print("CV hyperparameter to be tuned if needed")
tuned_parameters = [
    {'rf__n_estimators': [10, 25, 50, 100, 250, 500, 1000],
     # 'rf__max_depth': [10, 25, 50, 100, None]
     }
    ]
fb = FindBest(
    predictor,
    tuned_parameters=tuned_parameters, score='precision', cv=5)

# work on small dataset to tune paramters
limit_to_first_n = 2000
print("For computationnal time, we work with a reduced dataset.")
print("\twe take only the first %s samples." % limit_to_first_n)
bestpl = fb.find(
    X, y, X_test, y_test,
    limit=limit_to_first_n,
    report_results=True,
    # set to true if limit is big enough
    report_classification=True
    )


print("""
----------------------------
COMPUTATION WITH A PREDICTOR
----------------------------

I choose the predictor with 100 full grown trees.
""")

predictor = Pipeline([
        ('my_scaling', ms),
        ('rf', RandomForestClassifier(n_estimators=100,
                                      max_depth=None,
                                      n_jobs=-1))]
    )
# uncomment this, if you want to work with best pipeline
# predictor = bestpl
print("\n\nWE WORK WITH PREDICTOR :")
print(predictor)
print("fit predictor with hyperparameter %r"
      % predictor.steps[-1][1].get_params())
predictor.fit(X, y)

# SCORE ON TEST

score_report(predictor, X_test, y_test)

# PRINT MOST INFLUENTIAL INPUTS AND THEIR COEFS

coefs = predictor.steps[-1][1].feature_importances_
influence = most_influential(coefs, cols_interpret, thres=0.0)
report_influential(influence, nb=20, grouped=False)
report_influential(influence, nb=100, grouped=True)

