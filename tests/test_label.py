from learning.utils import DataHandler
from learning import label

from .mockutils import FMLTestCase


class PriceTest(FMLTestCase):
    @classmethod
    def setUpClass(cls):
        super(PriceTest, cls).setUpClass()
        cls.data = DataHandler().get_time_series_data("SPY")
        cls.close = cls.data["Close"]

    def test_daily_vol(self):
        price = label.Price(self.close["2016-06":"2016-12"])
        df = price.ewm_vol(20)
        self.assert_frame_equal(df, "close_ewm_vol")
