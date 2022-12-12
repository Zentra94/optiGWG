import unittest
from utils.optimization import (get_pred_by_gwg, get_gwg_interval_recommendation, plot_gwg_optimization,
                                get_gwg_interval_recommendations_from_features,
                                get_gwg_interval_recommendation_2T,
                                get_gwg_interval_recommendations_from_features_2T)
from utils.prediction import Predictor
from configs import PATH_DATA_INPUT, PATH_DATA_PLOTS_OPTIMIZATION
import pandas as pd


class TestOptimization(unittest.TestCase):
    gwg_range = [x for x in range(1, 26)]
    predictor = Predictor(targets=["IS_SICK"])
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
                              path=PATH_DATA_PLOTS_OPTIMIZATION / "test_IS_SICK.png",
                              interval_recommendation=gwg_interval_recommendation)

    def test_get_gwg_interval_recommendations_from_features(self):
        patients_features = pd.read_csv(PATH_DATA_INPUT / "01_process.csv", index_col=0, nrows=5)
        recommendations = get_gwg_interval_recommendations_from_features(patients_features=patients_features,
                                                                         predictor=self.predictor)
        self.assertEqual(len(recommendations), len(patients_features))

    predictor_2T = Predictor(targets=["diab_hiper"])
    weights_2T = {}
    for t in predictor_2T.targets:
        weights_2T[t] = 1 / len(predictor.targets)

    def test_get_pred_by_GWG_2T(self):
        pred_by_gwg = get_pred_by_gwg(predictor=self.predictor_2T,
                                      patient_features=self.patient_features,
                                      gwg_range=self.gwg_range,
                                      weights=self.weights_2T)

        self.assertEqual(len(pred_by_gwg), len(self.gwg_range))

    def test_gwg_interval_recommendation_2T(self):
        pred_by_gwg = get_pred_by_gwg(predictor=self.predictor_2T,
                                      patient_features=self.patient_features,
                                      gwg_range=self.gwg_range,
                                      weights=self.weights_2T)
        pred_by_gwg_const = get_pred_by_gwg(predictor=Predictor(targets=["LGA_SGA"]),
                                            patient_features=self.patient_features,
                                            gwg_range=self.gwg_range,
                                            weights={"LGA_SGA": [1]})

        gwg_interval_recommendation = get_gwg_interval_recommendation_2T(pred_by_gwg=pred_by_gwg,
                                                                         pred_by_gwg_const=pred_by_gwg_const,
                                                                         gwg_limit=5,
                                                                         pred_limit=0.05,
                                                                         const_th=0.18,
                                                                         )

        self.assertEqual(gwg_interval_recommendation["min_gwg"][0] > 0, True)

    def test_plot_gwg_optimization_2T(self):
        pred_by_gwg = get_pred_by_gwg(predictor=self.predictor_2T,
                                      patient_features=self.patient_features,
                                      gwg_range=self.gwg_range,
                                      weights=self.weights_2T)

        pred_by_gwg_const_LGA = get_pred_by_gwg(predictor=Predictor(targets=["LGA"]),
                                                patient_features=self.patient_features,
                                                gwg_range=self.gwg_range,
                                                weights={"LGA": [1]})

        pred_by_gwg_const_SGA = get_pred_by_gwg(predictor=Predictor(targets=["SGA"]),
                                                patient_features=self.patient_features,
                                                gwg_range=self.gwg_range,
                                                weights={"SGA": [1]})

        pred_by_gwg_const_LGA.rename(inplace=True, columns={"pred": "LGA"})
        pred_by_gwg_const_SGA.rename(inplace=True, columns={"pred": "SGA"})

        pred_by_gwg_const = pred_by_gwg_const_LGA.merge(pred_by_gwg_const_SGA, on="GWG")

        gwg_interval_recommendation = get_gwg_interval_recommendation_2T(pred_by_gwg=pred_by_gwg,
                                                                         pred_by_gwg_const=pred_by_gwg_const,
                                                                         gwg_limit=5,
                                                                         pred_limit=0.05,
                                                                         const_name1="LGA",
                                                                         const_name2="SGA",
                                                                         const_th1=0.18,
                                                                         const_th2=0.18)

        plot_gwg_optimization(pred_by_gwg=pred_by_gwg,
                              title="FO: diabetes & hipertension / CONST: LGA & SGA",
                              path=PATH_DATA_PLOTS_OPTIMIZATION / "test_2T.png",
                              interval_recommendation=gwg_interval_recommendation)

    def test_get_gwg_interval_recommendations_from_features_2T(self):
        patients_features = pd.read_csv(PATH_DATA_INPUT / "01_process.csv", index_col=0, nrows=5)
        recommendations = get_gwg_interval_recommendations_from_features_2T(patients_features=patients_features)
        self.assertEqual(len(recommendations), len(patients_features))


if __name__ == '__main__':
    unittest.main()
