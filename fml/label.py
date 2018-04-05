NUM_TRADING_DAYS = 252


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

    def triple_barrier_with_rolling_vol(
            self, window=20, upper_coef=1., lower_coef=1., vol_window=100):
        min_periods = 1
        vol = self.rolling_vol(vol_window, min_periods=min_periods)
        ret = self.pct_change
        rolling_mean = ret.rolling(vol_window, min_periods=min_periods).mean()
        upper_bound = rolling_mean + upper_coef * vol
        lower_bound = rolling_mean - lower_coef * vol
