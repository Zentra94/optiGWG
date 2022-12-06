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
            data = pd.read_csv(path, index_col=0, nrows=1)
            pred = predictor.predict(X=data, target_name=t)
            self.assertEqual(len(pred), len(data))

    def test_Predictor_IS_SICK(self):
        target = ["IS_SICK"]
        predictor = Predictor(targets=target)
        path = PATH_DATA_INPUT / "01_process.csv"
        data = pd.read_csv(path, index_col=0, nrows=1)
        pred = predictor.predict(X=data, target_name=target[0])

        self.assertEqual(len(pred), len(data))

    def test_Predictor_2T(self):
        target = ["diab_hiper", "LGA_SGA"]
        predictor = Predictor(targets=target)
        path = PATH_DATA_INPUT / "01_process.csv"
        data = pd.read_csv(path, index_col=0, nrows=1)
        pred = predictor.predict(X=data, target_name=target[0])

        self.assertEqual(len(pred), len(data))


if __name__ == '__main__':
    unittest.main()
