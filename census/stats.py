# -*- coding: utf-8 -*-
import pylab as P
from numpy import floor
from pandas import Index


class BasicStatistic(object):

    BARH_HEIGHT = 0.4  # inches
    BARH_FIG_WIDTH = 8  # inches

    """Docstring"""
    def __init__(self, df, non_valids=[], specials=[]):
        super(BasicStatistic, self).__init__()
        self.df = df
        self.non_valids = non_valids
        self.specials = specials

    # return the percentage dataframe of a numerical columns dataframe
    def percentage(self, num_df):
        return num_df.astype(float).div(num_df.sum(1), axis=0).fillna(0)

    # plot statistics of col when it is not numeric
    def plot_class_stat(self, col):
        t = self.count_values(col)
        idx_arrangements = [self.specials, self.non_valids]
        if idx_arrangements:
            t = self.arrange_reindex(t, idx_arrangements)
        fig, axes = P.subplots(2, 1,
                               figsize=(self.BARH_FIG_WIDTH,
                                        len(t)*self.BARH_HEIGHT + 2)
                               )
        t.plot(kind='barh', stacked=True, ax=axes[0])
        # percentage display
        t_perct = self.percentage(t)
        t_perct.plot(kind='barh', stacked=True, ax=axes[1])

    # plot statistic of col when numeric
    def plot_num_stat(self, col, stepped=None, legend=None):
        fig, axes = P.subplots(2, 1, figsize=(10, 7))
        t = self.count_values(col)
        t.plot(ax=axes[0])
        if stepped is not None:
            t = self.count_values(stepped)
        t_perct = t.astype(float).div(t.sum(1), axis=0)
        t_perct.plot(kind='bar', ax=axes[1], stacked=True)
        if legend:
            fig.text(0.15, 0.17, legend, color='red', fontweight='bold')
        if stepped is not None:
            fig.text(0.25, 0.05, "subdivision bins",
                     horizontalalignment='center')

    # change a continuous numerical columns dataframe
    # into a step function
    # When zero_aside is True, the step 0 is dedicated to value=0
    def stepped(self, col_df, step_nb, zero_aside=False):
        col_df = col_df.astype(float)
        stage = (col_df.max() + 1) / step_nb
        if zero_aside:
            col_df = col_df - 1.0
        col_df = floor(col_df / stage)
        legend = None
        if zero_aside:
            col_df = col_df + 1
            legend = '0\'th bin contains\nonly values zero.'
        return col_df, legend

    # get the table counting pairs (col_value, TARGET_value)
    def count_values(self, col):
        grouped = self.df.groupby([col, 'TARGET'])
        return grouped.size().unstack().fillna(0)

    # reindex a class col_df
    # All index items appearing in the idx_arrangements at the end
    def arrange_reindex(self, col_df, idx_arrangements=[]):
        new_index = []
        for a in idx_arrangements:
            new_index += [i for i in col_df.index if i in a]
        new_index = Index([i for i in col_df.index if i not in new_index]
                          + new_index)
        return col_df.reindex(new_index)
