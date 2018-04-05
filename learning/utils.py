from os import path
import pandas as pd


class DataHandler(object):
    def __init__(self):
        self.data_dir = path.join(path.dirname(__file__), "..", "data")

    def get_time_series_data(self, ticker):
        filename = path.join(self.data_dir, ticker + ".csv")
        return read_ts_csv(filename)


def read_ts_csv(filename):
    return pd.read_csv(filename, header=0, parse_dates=True, index_col=0)
