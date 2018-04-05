class DailyPrice(object):
    def __init__(self, price_series):
        self.data = price_series

    @property
    def pct_change(self):
        return self.data.asfreq("B", method="pad").pct_change()

    def ewm_vol(self, span=100):
        return self.pct_change.ewm(span=span).std()

    def rolling_vol(self, window=100):
        return self.pct_change.rolling(window).std()
