from os import path
from unittest import TestCase

import pandas as pd
import pandas.util.testing as pdt
import sheepts


class FMLTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ref_dir = path.join(path.dirname(__file__), "ref")

    def assert_frame_equal(self, df, name, generate_ref=False, precision=10):
        df = df if isinstance(df, pd.DataFrame) else df.to_frame()
        df.columns = df.columns.astype(str)
        df = df.round(precision)
        filename = path.join(self.ref_dir, name + ".csv")
        if generate_ref:
            df.to_csv(filename)
        else:
            df_ref = sheepts.read_time_series_csv(filename)
            pdt.assert_frame_equal(df_ref, df, check_less_precise=precision)
