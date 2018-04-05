class Price(object):
    def __init__(self, price_series):
        self.data = price_series

    @property
    def daily_ret(self):
        return self.data.asfreq("B", method="pad").pct_change()

    def daily_ewm_vol(self, span=100):
        return self.daily_ret.ewm(span=span).std()

    def daily_rolling_vol(self, window=100):
        return self.daily_ret.rolling(window).std()
