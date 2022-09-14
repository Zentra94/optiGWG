import unittest
from preprocess import fix_binaries
from utils.reader import get_input_df, get_catalog


class TestPreprocess(unittest.TestCase):
    def test_fix_binaries(self):
        self.assertEqual(fix_binaries("VERDADERO"), 1)  # add assertion here
        catalog = get_catalog()
        bin_cols = catalog.loc[catalog["type"] == "boolean", "name"]
        raw_data = get_input_df(file="00_raw", n_rows=10)

        for c in bin_cols:
            raw_data[c] = raw_data[c].apply(lambda x: fix_binaries(x))


if __name__ == '__main__':
    unittest.main()
