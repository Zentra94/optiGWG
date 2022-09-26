import unittest
import pandas as pd
from utils.prediction import Predictor
from configs import PATH_DATA_INPUT


class TestPrediction(unittest.TestCase):
    def test_Predictor(self):
        predictor = Predictor()
        targets = predictor.targets
        for t in targets:
            path = PATH_DATA_INPUT / "01_preprocess_balanced_{}.csv".format(t)
            data = pd.read_csv(path, index_col=0, nrows=5)
            pred = predictor.predict(X=data, target_name=t)

            self.assertEqual(len(pred), len(data))


if __name__ == '__main__':
    unittest.main()
