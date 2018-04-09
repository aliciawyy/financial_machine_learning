import operator
import pandas as pd
import sheepts


class Price(object):
    def __init__(self, price_series, freq="B"):
        self.data = price_series
        self.freq = freq

    @sheepts.lazy_property
    def clean_data(self):
        data = self.data.asfreq(freq=self.freq) if self.freq else self.data
        return data.fillna(method="pad")

    def pct_change(self, periods=1):
        return self.clean_data.pct_change(periods=periods)

    def ewm_vol(self, span=100):
        return self.pct_change().ewm(span=span).std()

    def rolling_vol(self, window=100, min_periods=None):
        return self.pct_change().rolling(window, min_periods=min_periods).std()

    def rolling_bounds(
            self, window=100, min_periods=1, upper_coef=1., lower_coef=1.,
            with_mean=True):
        vol = self.rolling_vol(window, min_periods=min_periods)
        offset = 0.
        if with_mean:
            ret = self.pct_change()
            offset = ret.rolling(window, min_periods=min_periods).mean()
        return pd.concat({
            "upper_bound": offset + upper_coef * vol,
            "lower_bound": offset - lower_coef * vol
        }, axis=1)

    def future_ret_window_view(self, window=10):
        cols = list(range(1, window + 1))
        df = pd.concat({i: self.pct_change(i).shift(-i) for i in cols}, axis=1)
        return df[cols]

    def triple_barrier(self, window=10, bounds=None, n_labels=2):
        """
        Returns a boolean Series when n_labels = 2:
            True if the upper bound is touched first in the window;
            False if lower bound is touched first.
            When no bound is touched, return the sign of the perf within the
            window range.

        """
        cross_time = self.bounds_cross_time(window, bounds)
        label = cross_time["upper_bound"] < cross_time["lower_bound"]

        is_no_touch = cross_time["upper_bound"] == cross_time["lower_bound"]
        if n_labels == 2:
            ret = self.pct_change(window).shift(-window)
            no_touch_labels = ret.loc[is_no_touch] > 0
        else:
            label = label.map({True: 1, False: -1})
            no_touch_labels = 0
        label.loc[is_no_touch] = no_touch_labels
        return label

    def bounds_cross_time(self, window=10, bounds=None):
        if bounds is None:
            bounds = self.rolling_bounds()
        df = self.future_ret_window_view(window)
        df = df.join(bounds)
        return pd.concat({
            side: sheepts.apply_by_multiprocessing(
                df, _CrossTime(window, side), axis=1
            )
            for side in ["lower_bound", "upper_bound"]
        }, axis=1)

    def num_concurrent_events(self, window=10, bounds=None):
        cross_time = self.bounds_cross_time(window, bounds)
        df = cross_time.min(axis=1).to_frame("cross")
        windows = list(range(1, window + 2))
        for win in windows:
            df[win] = df["cross"].shift(win) >= win
        return df[windows].sum(axis=1).rename("num_concurrent_events")


class _CrossTime(sheepts.StringMixin):
    def __init__(self, window, side="upper_bound"):
        self.window_limit = window + 1
        self.side = side

    @sheepts.lazy_property
    def compare(self):
        return operator.gt if self.side == "upper_bound" else operator.lt

    @sheepts.lazy_property
    def window_cols(self):
        return list(range(1, self.window_limit))

    def __call__(self, row):
        is_cross = self.compare(row.loc[self.window_cols], row[self.side])
        cross_times = is_cross[is_cross].index
        return self.window_limit if len(cross_times) == 0 else cross_times[0]
