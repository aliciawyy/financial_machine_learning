from os import path
from unittest import TestCase

from sheepts import testing


class FMLTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ref_dir = path.join(path.dirname(__file__), "ref")

    def assert_frame_equal(self, df, name, generate_ref=False, precision=10):
        filename = path.join(self.ref_dir, name + ".csv")
        testing.assert_ts_frame_equal(
            df, filename, generate_ref=generate_ref, precision=precision
        )
