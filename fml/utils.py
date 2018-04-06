from os import path

import sheepts


class DataHandler(sheepts.CsvDataHandler):
    def __init__(self):
        data_dir = path.join(path.dirname(__file__), "..", "data")
        super(DataHandler, self).__init__(data_dir)
