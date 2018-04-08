from os import path

from sheepts import testing


class FMLTestCase(testing.TsTestCase):

    @classmethod
    def get_ref_dir(cls):
        return path.join(path.dirname(__file__), "ref")
