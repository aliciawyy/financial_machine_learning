import pandas as pd
import sheepts


class DailyPrice(object):
    def __init__(self, price_series):
        self.data = price_series

    @sheepts.lazy_property
    def clean_data(self):
        return self.data.asfreq("B", method="pad")

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

    def triple_barrier(
            self, window=20, upper_coef=1., lower_coef=1., vol_window=100):
        df = self.rolling_bounds(
            vol_window, upper_coef=upper_coef, lower_coef=lower_coef
        )
