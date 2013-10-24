# -*- coding: utf-8 -*-
import pylab as P
from numpy import floor
from pandas import Index, concat


class BasicStatistic(object):

    BARH_HEIGHT = 0.4  # inches
    BARH_FIG_WIDTH = 8  # inches

    """Docstring"""
    def __init__(self, non_valids=[], specials=[]):
        super(BasicStatistic, self).__init__()
        self.non_valids = non_valids
        self.specials = specials

    # return the percentage dataframe of a numerical columns dataframe
    def percentage(self, num_df, label=None):
        return num_df.astype(float).div(num_df.sum(1), axis=0).fillna(0)

    # plot statistics of col when it is not numeric
    # col_df, group_by are columns dataframe of same height
    def plot_cat_stat(self, col_df, group_by, label=''):
        # plot raw data
        t = self.count_values_per_target(col_df, group_by)
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
        self.add_col_desc(fig, col_df.name, label=label)

    # plot statistic of col when numeric
    # col_df, group_by are columns dataframe of same height
    # perct_steps is of number bins for percentage plot
    def plot_num_stat(self, col_df, group_by, no_plot_zero=False,
                      perct_steps=0, perct_zero_aside=False, label=''
                      ):
        fig, axes = P.subplots(2, 1, figsize=(10, 7))
        ax_raw, ax_perct = tuple(axes)
        self.plot_num_stat_raw(
            col_df, group_by, no_plot_zero=no_plot_zero, ax=ax_raw)
        self.plot_num_stat_perct(col_df, group_by,
                                 steps=perct_steps,
                                 zero_aside=perct_zero_aside,
                                 ax=ax_perct)
        self.add_col_desc(fig, col_df.name, label)

    def plot_num_stat_raw(self, col_df, group_by, no_plot_zero=False, ax=None):
        t = self.count_values_per_target(col_df, group_by)
        if no_plot_zero:
            zeros_nb = sum(t.ix[0])
            t = t.ix[t.index != 0]
        t.plot(ax=ax, marker='o')
        ax.set_xlabel("raw data")
        if no_plot_zero:
            ax.set_ylabel("zero value not plotted :\n%d" % (zeros_nb),
                          color='red', fontweight='bold')

    def plot_num_stat_perct(self, col_df, group_by,
                            steps=0, zero_aside=False, ax=None):
        if steps > 0:
            perct_col, legend = \
                self.stepped(col_df, steps, zero_aside=zero_aside)
            t = self.count_values_per_target(perct_col, group_by)
        else:
            t = self.count_values_per_target(col_df, group_by)
            legend = None
        t_perct = t.astype(float).div(t.sum(1), axis=0)
        t_perct.plot(kind='bar', ax=ax, stacked=True)
        if legend:
            ax.text(0.15, 0.17, legend, color='red', fontweight='bold')
        if steps > 0:
            ax.set_xlabel("subdivision bins")

    def add_col_desc(self, fig, string, label=''):
        if label != '':
            label = "(%s)" % label
        fig.text(0, 0.95, "%s %s" % (string, label),
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
    def count_values_per_target(self, col, group_by):
        df = concat([col, group_by], axis=1)
        grouped = df.groupby([col.name, group_by.name])
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
