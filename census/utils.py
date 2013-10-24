# -*- coding: utf-8 -*-


# return indices of col_name in cols
def cols_name_to_indices(cols, cols_name):
    num_cols_indices = []
    for col in cols_name:
        for i, v in enumerate(cols):
            if v == col:
                num_cols_indices += [i]
    return num_cols_indices


# return col_name of indices in cols_indices
def indices_to_cols_name(cols, cols_indices):
    cols_name = []
    for i in cols_indices:
        for j, v in enumerate(cols):
            if i == j:
                cols_name += [v]
    return cols_name
