# -*- coding: utf-8 -*-
import pylab as P
from numpy import floor
from pandas import Index


class BasicStatistic(object):

    BARH_HEIGHT = 0.4  # inches
    BARH_FIG_WIDTH = 8  # inches

    """Docstring"""
    def __init__(self, df, non_valids=[], specials=[], cols_desc={}):
        super(BasicStatistic, self).__init__()
        self.df = df
        self.non_valids = non_valids
        self.specials = specials
        self.cols_desc = cols_desc

    # return the percentage dataframe of a numerical columns dataframe
    def percentage(self, num_df):
        return num_df.astype(float).div(num_df.sum(1), axis=0).fillna(0)

    # plot statistics of col when it is not numeric
    # col is a string
    def plot_class_stat(self, col):
        # plot raw data
        t = self.count_values_per_target(col)
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
        # add some text for infos
        self.add_col_desc(fig, col)

    # plot statistic of col when numeric
    # col is a string
    # perct_col is a col dataframe
    # perct_legend is a string
    def plot_num_stat(self, col,
                      perct_col=None, perct_legend=None,
                      no_plot_zero=False):
        # plot raw data
        fig, axes = P.subplots(2, 1, figsize=(10, 7))
        ax_raw, ax_perct = tuple(axes)
        t = self.count_values_per_target(col)
        if no_plot_zero:
            zeros_nb = sum(t.ix[0])
            t = t.ix[t.index != 0]
        t.plot(ax=ax_raw, marker='o')
        ax_raw.set_xlabel("raw data")
        if no_plot_zero:
            ax_raw.set_ylabel("zero value not plotted : %d" % (zeros_nb),
                              color='red', fontweight='bold')
        # plot percentage data (perct_col if needed)
        if perct_col is not None:
            t = self.count_values_per_target(perct_col)
        t_perct = t.astype(float).div(t.sum(1), axis=0)
        t_perct.plot(kind='bar', ax=ax_perct, stacked=True)
        self.add_col_desc(fig, col)
        if perct_legend:
            ax_perct.text(0.15, 0.17, perct_legend, color='red', fontweight='bold')
        if perct_col is not None:
            ax_perct.set_xlabel("subdivision bins")

    def add_col_desc(self, fig, col):
        fig.text(0, 0.95, "%s (%s)" % (col, self.cols_desc[col]),
                 # horizontalalignment='center',
                 fontweight='bold',
                 fontsize=14)

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
            legend = '0\'th bin contains\nonly value zero.'
        return col_df, legend

    # get the table counting pairs (col_value, TARGET_value)
    def count_values_per_target(self, col):
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
