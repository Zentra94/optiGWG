import unittest
from reader import get_input_df

class TestReader(unittest.TestCase):
    def test_get_input_df(self):
        files = ("00_raw", "01_process")
        for file in files:
            df = get_input_df(file=file, n_rows=100)
            self.assertEqual(df.empty, False)


if __name__ == '__main__':
    unittest.main()
