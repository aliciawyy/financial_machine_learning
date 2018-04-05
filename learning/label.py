import pandas as pd


class Price(object):
    def __init__(self, price_series):
        self.data = price_series

    def ewm_vol(self, span=100):
        price = self.data
        df = price.index.searchsorted(price.index - pd.Timedelta(days=1))
        df = df[df > 0]
        df = pd.Series(price.index[df - 1], index=price.index[price.shape[0] - df.shape[0]:])
        df1 = price.loc[df.index] / price.loc[df.values].values - 1
        return df1.ewm(span=span).std()
