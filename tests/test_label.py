from parameterized import parameterized
from fml.utils import DataHandler
from fml import label

from .mockutils import FMLTestCase


class DailyPriceTest(FMLTestCase):

    @classmethod
    def setUpClass(cls):
        super(DailyPriceTest, cls).setUpClass()
        cls.data = DataHandler().get_time_series_data("SPY")
        cls.close = cls.data["Adj Close"]

    def test_ewm_vol(self):
        price = label.DailyPrice(self.close["2016-06":"2016-12"])
        df = price.ewm_vol(50)
        self.assert_frame_equal(df, "ret_ewm_vol")

    def test_daily_rolling_vol(self):
        price = label.DailyPrice(self.close["2016-06":"2016-12"])
        df = price.rolling_vol(50)
        self.assert_frame_equal(df, "ret_rolling_vol")

    @parameterized.expand([("with_mean", True), ("without_mean", False)])
    def test_rolling_bounds(self, name, with_mean):
        price = label.DailyPrice(self.close[:"1993-06"])
        df = price.rolling_bounds(with_mean=with_mean)
        self.assert_frame_equal(df, "ret_rolling_bounds_" + name)

    def test_future_ret_window_view(self):
        price = label.DailyPrice(self.close["1993-06"])
        df = price.future_ret_window_view()
        self.assert_frame_equal(df, "ret_future_ret_window_view")
