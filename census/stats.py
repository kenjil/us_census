# -*- coding: utf-8 -*-
import pylab as P


class BasicStatistic(object):

    FIG_SIZE = (18, 200)  # inches
    FIG_COLS = 3
    FIG_LINES = 42

    """Basic statistics utils for Numerical Census DataFrame"""
    def __init__(self, df,
                 fig_size=FIG_SIZE,
                 fig_cols=FIG_COLS,
                 fig_lines=FIG_LINES,
                 cols_infos={}):
        super(BasicStatistic, self).__init__()
        # Data
        self.df = df
        self.cols_infos = cols_infos
        # put in memory
        self.cols_values = self.__cols_values()
        self.df_splitted = self.__split_on_target()
        # figure
        self.fig_size = fig_size
        self.fig_cols = fig_cols
        self.fig_lines = fig_lines

    # split df into as many df as there's value in target
    def __split_on_target(self):
        splitted = {}
        for v in self.df['TARGET'].unique():
            splitted[v] = self.df[self.df['TARGET'] == v]
        return splitted.values()

    # dict of col's unique values
    def __cols_values(self):
        cols_values = {}
        for col in self.df.columns:
            cols_values[col] = self.df[col].unique()
        return cols_values

    def __plot_stats_raw(self, col, max_bins=100):
        bins = min(len(self.cols_values[col]), max_bins)
        P.hist(self.__splitted(col), bins=bins, histtype='barstacked')
        P.title("%s raw data" % col)

    def __plot_stats_no_na(self, col, max_bins=100):
        x = self.__splitted(col)
        x = [s[s >= 0] for s in x]
        col_values = [v for v in self.cols_values[col] if v >= 0]
        bins = min(len(col_values), max_bins)
        P.hist(x, bins=bins, histtype='barstacked')
        P.title("%s with non meaningfull removed" % col)

    def __plot_desc(self, col, max_bins=100):
        if col in self.cols_infos:
            lines_nb = self.cols_infos[col].count("\n") + 1
            if lines_nb > 18:
                fontsize = 180 / lines_nb
            else:
                fontsize = 10
            P.text(0.05, 0.5, self.cols_infos[col],
                   verticalalignment='center',
                   fontsize=fontsize)
                # style='italic',
                # bbox={'facecolor':'red', 'alpha':0.5, 'pad':10}
            P.title("%s infos" % col)

    # returns a list of series of the splitted dfs for columns col
    def __splitted(self, col):
        return [df[col] for df in self.df_splitted]

    def plot_all_stats(self):
        P.figure(figsize=self.fig_size)

        fig_pos = 0
        for col in self.df.columns:
            fig_pos = self.plot_stats(col, fig_pos=fig_pos)

    def plot_stats(self, col, max_bins=100, fig_pos=None):
        # when called alone
        if fig_pos is None:
            fig_lines = 1
            fig_cols = 3
            fig_size = (18, 4)
            fig_pos = 0
            P.figure(num=col, figsize=fig_size)
        else:
            fig_lines = self.fig_lines
            fig_cols = self.fig_cols

        # raw stats
        fig_pos += 1
        P.subplot(fig_lines, fig_cols, fig_pos)
        self.__plot_stats_raw(col)

        # col infos
        fig_pos += 1
        P.subplot(fig_lines, fig_cols, fig_pos)
        self.__plot_desc(col)

        # non meaningfull data removed stats
        fig_pos += 1
        if len([v for v in self.cols_values[col] if v < 0]) > 0:
            P.subplot(fig_lines, fig_cols, fig_pos)
            self.__plot_stats_no_na(col)
        return fig_pos
