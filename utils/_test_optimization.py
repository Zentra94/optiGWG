import unittest
from utils.optimization import get_pred_by_gwg, get_gwg_interval_recommendation, plot_gwg_optimization
from utils.prediction import Predictor
from configs import PATH_DATA_INPUT, PATH_DATA_PLOTS_OPTIMIZATION
import pandas as pd


class TestOptimization(unittest.TestCase):
    gwg_range = [x for x in range(1, 26)]
    predictor = Predictor()
    weights = {}
    for t in predictor.targets:
        weights[t] = 1 / len(predictor.targets)
    patient_features = pd.read_csv(PATH_DATA_INPUT / "01_process.csv", index_col=0, nrows=1)

    def test_get_pred_by_GWG(self):

        pred_by_gwg = get_pred_by_gwg(predictor=self.predictor,
                                      patient_features=self.patient_features,
                                      gwg_range=self.gwg_range,
                                      weights=self.weights)

        self.assertEqual(len(pred_by_gwg), len(self.gwg_range))

    def test_gwg_interval_recommendation(self):

        pred_by_gwg = get_pred_by_gwg(predictor=self.predictor,
                                      patient_features=self.patient_features,
                                      gwg_range=self.gwg_range,
                                      weights=self.weights)

        gwg_interval_recommendation = get_gwg_interval_recommendation(pred_by_gwg=pred_by_gwg,
                                                                      gwg_limit=5,
                                                                      pred_limit=0.05)

        self.assertEqual(gwg_interval_recommendation["min_gwg"][0] > 0, True)

    def test_plot_gwg_optimization(self):
        pred_by_gwg = get_pred_by_gwg(predictor=self.predictor,
                                      patient_features=self.patient_features,
                                      gwg_range=self.gwg_range,
                                      weights=self.weights)
        gwg_interval_recommendation = get_gwg_interval_recommendation(pred_by_gwg=pred_by_gwg,
                                                                      gwg_limit=5,
                                                                      pred_limit=0.005)

        plot_gwg_optimization(pred_by_gwg=pred_by_gwg,
                              path=PATH_DATA_PLOTS_OPTIMIZATION/"test.png",
                              interval_recommendation=gwg_interval_recommendation)


if __name__ == '__main__':
    unittest.main()
