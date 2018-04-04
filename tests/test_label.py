from unittest import TestCase
from learning import label

from .mockutils import MockDataHandler


class DailyVolTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = MockDataHandler().get_time_series_data("SPY")

    def test_daily_vol(self):
        assert "Close" in self.data.columns
