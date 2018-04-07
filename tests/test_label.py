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
        cls.price_small = label.DailyPrice(cls.close[:"1993-06"])

    @parameterized.expand(["ewm_vol", "rolling_vol"])
    def test_vol(self, method_name):
        price = label.DailyPrice(self.close["2016-06":"2016-12"])
        df = getattr(price, method_name)(50)
        self.assert_frame_equal(df, "ret_" + method_name)

    @parameterized.expand([("with_mean", True), ("without_mean", False)])
    def test_rolling_bounds(self, name, with_mean):
        df = self.price_small.rolling_bounds(with_mean=with_mean)
        self.assert_frame_equal(df, "ret_rolling_bounds_" + name)

    def test_future_ret_window_view(self):
        price = label.DailyPrice(self.close["1993-06"])
        df = price.future_ret_window_view()
        self.assert_frame_equal(df, "ret_future_ret_window_view")

    def test_triple_barrier(self):
        df = self.price_small.triple_barrier(window=20)
        self.assert_frame_equal(df, "ret_triple_barrier")

    def test_bounds_cross_time(self):
        df = self.price_small.bounds_cross_time()
        self.assert_frame_equal(df, "ret_bounds_cross_time")
