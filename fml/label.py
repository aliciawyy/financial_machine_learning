import pandas as pd


class DailyPrice(object):
    def __init__(self, price_series):
        self.data = price_series

    @property
    def pct_change(self):
        return self.data.asfreq("B", method="pad").pct_change()

    def ewm_vol(self, span=100):
        return self.pct_change.ewm(span=span).std()

    def rolling_vol(self, window=100, min_periods=None):
        return self.pct_change.rolling(window, min_periods=min_periods).std()

    def rolling_bounds(
            self, window=100, min_periods=1, upper_coef=1., lower_coef=1.):
        vol = self.rolling_vol(window, min_periods=min_periods)
        ret = self.pct_change
        rolling_mean = ret.rolling(window, min_periods=min_periods).mean()
        return pd.concat({
            "upper_bound": rolling_mean + upper_coef * vol,
            "lower_bound": rolling_mean - lower_coef * vol
        }, axis=1)

    def ret_window_view(self, window):
        pass

    def triple_barrier(
            self, window=20, upper_coef=1., lower_coef=1., vol_window=100):
        df = self.rolling_bounds(
            vol_window, upper_coef=upper_coef, lower_coef=lower_coef
        )
