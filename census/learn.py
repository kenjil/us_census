# -*- coding: utf-8 -*-
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from numpy import arange
import re


class FindBest(object):
    """docstring for Finn"""
    def __init__(self, predictor, tuned_parameters, score='precision', cv=2):
        super(FindBest, self).__init__()
        self.tuned_parameters = tuned_parameters
        self.predictor = predictor
        # score can be 'f1', 'average_precision'
        self.score = score
        self.cv = cv
                        
    def find(self, X, y, X_test, y_test, limit=0,
             report_results=False, report_classification=False):
        if limit > 0:
            # work on small dataset
            # n = X.shape[0]
            X = X[:limit]
            X_test = X_test[:limit]
            y = y[:limit]
            y_test = y_test[:limit]

        print("We're using score '%s'." % self.score)
        clf = GridSearchCV(
            self.predictor, self.tuned_parameters, cv=self.cv,
            scoring=self.score, n_jobs=-1)
        clf.fit(X, y)
        self._report_results(clf.grid_scores_)
        print("Best predictor is\n")
        print(clf.best_estimator_)
        score_report(clf, X_test, y_test)
        return clf.best_estimator_

    def _report_results(self, clf_grid_scores):
        for params, mean_score, scores in clf_grid_scores:
            print(
                "%0.3f (+/-%0.03f) for %r"
                % (mean_score, scores.std() * 2, params))
        print("")


# print score of a predictor
def score_report(predictor, X, y):
    print("predictor score on test")
    y_true, y_pred = y, predictor.predict(X)
    print(classification_report(y_true, y_pred))


# return a list of cols item with their correcponding coef
def most_influential(coefs, cols, thres=0):
    id = arange(len(coefs))
    id_ok = id[abs(coefs) >= thres]
    stack = []
    for i in id_ok:
        stack += [(cols[i], coefs[i])]
    return stack


# print most influential factors
def report_influential(infl, nb=50, grouped=False):
    print("\nTHE MOST INFLUENTIAL FACTS")
    if grouped is True:
        print("Sorted by max coef within each group\n")
        # build the index to sort by group
        # find category
        cat_re = re.compile('^[^\s]*')
        sort_idx = _build_sort_index(infl, cat_re)

        # x -> category_of_x then abs(coef_of_x)
        def sort_key(x):
            cat = cat_re.search(x[0]).group()
            return "%s%s" % (sort_idx[cat], abs(x[1]))

        infl.sort(key=sort_key, reverse=True)
    else:
        print("Sorted by coef\n")
        infl.sort(key=lambda x: abs(x[1]), reverse=True)
    for c in infl[:nb]:
        print " - %s : %s" % (c[0], c[1])


# build the category sort index
# used in report_influential when grouped
def _build_sort_index(infl, regexp):
    sort_index = {}
    for col, v in infl:
        col = regexp.search(col).group()
        sort_index.setdefault(col, 0)
        sort_index[col] = max(sort_index[col], abs(v))
    return sort_index



