from learning.utils import DataHandler
from learning import label

from .mockutils import FMLTestCase


class DailyPriceTest(FMLTestCase):

    @classmethod
    def setUpClass(cls):
        super(DailyPriceTest, cls).setUpClass()
        cls.data = DataHandler().get_time_series_data("SPY")
        cls.close = cls.data["Close"]

    def test_ewm_vol(self):
        price = label.DailyPrice(self.close["2016-06":"2016-12"])
        df = price.ewm_vol(50)
        self.assert_frame_equal(df, "close_ewm_vol")

    def test_daily_rolling_vol(self):
        price = label.DailyPrice(self.close["2016-06":"2016-12"])
        df = price.rolling_vol(50)
        self.assert_frame_equal(df, "close_rolling_vol")
