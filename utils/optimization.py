import pandas as pd
import matplotlib.pyplot as plt
from utils.prediction import Predictor
import time
from datetime import timedelta


def get_pred_by_gwg(patient_features, predictor=None, gwg_range=None, weights=None):
    if predictor is None:
        predictor = Predictor()
    if gwg_range is None:
        gwg_range = [x for x in range(1, 26)]
    if weights is None:
        weights = {}
        for t in predictor.targets:
            weights[t] = 1 / len(predictor.targets)

    pred_by_gwg = pd.DataFrame()
    pred_by_gwg["GWG"] = gwg_range
    targets = predictor.targets

    for t in targets:
        features = predictor.features_names[t]
        aux_data = pd.DataFrame()
        aux_data = aux_data.append([patient_features[features].drop(columns="GWG")] * len(gwg_range))
        aux_data["GWG"] = gwg_range
        pred_by_gwg[t] = predictor.predict(X=aux_data, target_name=t) * weights[t]

    pred_by_gwg["pred"] = pred_by_gwg.loc[:, targets].sum(axis=1)
    pred_by_gwg.drop(columns=targets, inplace=True)

    return pred_by_gwg


def plot_gwg_optimization(pred_by_gwg, interval_recommendation=None, path=None, title=None):
    if title is None:
        title = "GWG optimization"

    plt.subplots(figsize=(15, 8))
    plt.plot(pred_by_gwg["GWG"], pred_by_gwg["pred"])
    plt.plot(interval_recommendation["best_gwg"][0], interval_recommendation["best_gwg"][1],
             c="r", marker='o', markeredgecolor="red", label="best GWG")
    plt.axvline(x=interval_recommendation["min_gwg"][0], color='r', label='min GWG',
                linestyle="dashed", linewidth=1, alpha=0.8)
    plt.axvline(x=interval_recommendation["max_gwg"][0], color='r', label='max GWG',
                linestyle="dashed", linewidth=1, alpha=0.8)
    plt.xticks(ticks=pred_by_gwg["GWG"])
    plt.grid(True)
    plt.title(title)
    plt.savefig(path)


def get_gwg_interval_recommendation(pred_by_gwg, gwg_limit=3, pred_limit=0.05):
    best_idx = pred_by_gwg["pred"].idxmin()
    best_gwg = pred_by_gwg.loc[best_idx, "GWG"]
    best_pred = pred_by_gwg.loc[best_idx, "pred"]

    min_idx = best_idx
    min_gwg = best_gwg
    min_pred = best_pred

    while min_idx - 1 in pred_by_gwg.index and abs(min_gwg - best_gwg) < gwg_limit and abs(
            min_pred - best_pred) < pred_limit:
        min_idx += -1
        min_gwg = pred_by_gwg.loc[min_idx, "GWG"]
        min_pred = pred_by_gwg.loc[min_idx, "pred"]

    max_idx = best_idx
    max_gwg = best_gwg
    max_pred = best_pred

    while max_idx + 1 in pred_by_gwg.index and abs(max_gwg - best_gwg) < gwg_limit and abs(
            max_pred - best_pred) < pred_limit:
        max_idx += +1
        max_gwg = pred_by_gwg.loc[max_idx, "GWG"]
        max_pred = pred_by_gwg.loc[max_idx, "pred"]

    return {"min_gwg": (min_gwg, min_pred), "max_gwg": (max_gwg, max_pred), "best_gwg": (best_gwg, best_pred)}


def get_gwg_interval_recommendations_from_features(patients_features, gwg_limit=3, pred_limit=0.05, predictor=None,
                                                   gwg_range=None, weights=None):
    gwg_interval_recommendations = pd.DataFrame()

    ti = time.time()

    for i in patients_features.index:

        patient_features = patients_features.loc[i, :].to_frame().T

        pred_by_gwg = get_pred_by_gwg(predictor=predictor,
                                      patient_features=patient_features,
                                      gwg_range=gwg_range,
                                      weights=weights)

        gwg_interval_recommendation = get_gwg_interval_recommendation(pred_by_gwg=pred_by_gwg,
                                                                      gwg_limit=gwg_limit,
                                                                      pred_limit=pred_limit)
        recom_fmt = {}

        for k in gwg_interval_recommendation:
            recom_fmt["{}_GWG".format(k)] = gwg_interval_recommendation[k][0]
            recom_fmt["{}_score".format(k)] = gwg_interval_recommendation[k][1]

        gwg_interval_recommendations = gwg_interval_recommendations.append(recom_fmt,
                                                                           ignore_index=True)

    tf = time.time()
    df = timedelta(seconds=tf - ti)

    print("Total time {} to process {} obs".format(df, len(patients_features)))

    return gwg_interval_recommendations


def get_gwg_interval_recommendation_2T(pred_by_gwg,
                                       pred_by_gwg_const,
                                       const_name1="LGA",
                                       const_name2="SGA",
                                       gwg_limit=3,
                                       pred_limit=0.05,
                                       const_th1=0.1,
                                       const_th2=0.1):
    mask = (pred_by_gwg_const[const_name1] < const_th1) & (pred_by_gwg_const[const_name2] < const_th2)
    if pred_by_gwg[mask].empty:
        return {"min_gwg": (None, None), "max_gwg": (None, None), "best_gwg": (None, None)}

    best_idx = pred_by_gwg[mask]["pred"].idxmin()
    best_gwg = pred_by_gwg.loc[best_idx, "GWG"]
    best_pred = pred_by_gwg.loc[best_idx, "pred"]

    min_idx = best_idx
    min_gwg = best_gwg
    min_pred = best_pred

    current_const1 = pred_by_gwg_const.loc[min_idx, const_name1]
    current_const2 = pred_by_gwg_const.loc[min_idx, const_name2]

    while min_idx - 1 in pred_by_gwg.index and abs(min_gwg - best_gwg) < gwg_limit and abs(
            min_pred - best_pred) < pred_limit and current_const1 < const_th1 and current_const2 < const_th2:
        min_idx += -1
        min_gwg = pred_by_gwg.loc[min_idx, "GWG"]
        min_pred = pred_by_gwg.loc[min_idx, "pred"]

        current_const1 = pred_by_gwg_const.loc[min_idx, const_name1]
        current_const2 = pred_by_gwg_const.loc[min_idx, const_name2]

    max_idx = best_idx
    max_gwg = best_gwg
    max_pred = best_pred
    current_const1 = pred_by_gwg_const.loc[max_idx, const_name1]
    current_const2 = pred_by_gwg_const.loc[max_idx, const_name2]

    while max_idx + 1 in pred_by_gwg.index and abs(max_gwg - best_gwg) < gwg_limit and abs(
            max_pred - best_pred) < pred_limit and current_const1 < const_th1 and current_const2 < const_th2:
        max_idx += +1
        max_gwg = pred_by_gwg.loc[max_idx, "GWG"]
        max_pred = pred_by_gwg.loc[max_idx, "pred"]

        current_const1 = pred_by_gwg_const.loc[max_idx, const_name1]
        current_const2 = pred_by_gwg_const.loc[max_idx, const_name2]

    return {"min_gwg": (min_gwg, min_pred), "max_gwg": (max_gwg, max_pred), "best_gwg": (best_gwg, best_pred)}


def get_gwg_interval_recommendations_from_features_2T(patients_features,
                                                      gwg_limit=3,
                                                      pred_limit=0.05,
                                                      const_th1=0.1,
                                                      const_name1="LGA",
                                                      const_name2="SGA",
                                                      const_th2=0.1,
                                                      predictor=None,
                                                      predictor_const=None,
                                                      gwg_range=None):
    gwg_interval_recommendations = pd.DataFrame()

    if not predictor:
        predictor = Predictor(targets=["diab_hiper"])
    if not predictor_const:
        predictor_const = Predictor(targets=["LGA_SGA"])

    ti = time.time()

    for i in patients_features.index:

        patient_features = patients_features.loc[i, :].to_frame().T

        pred_by_gwg = get_pred_by_gwg(predictor=predictor,
                                      patient_features=patient_features,
                                      gwg_range=gwg_range)

        pred_by_gwg_const_LGA = get_pred_by_gwg(predictor=Predictor(targets=[const_name1]),
                                                patient_features=patient_features,
                                                gwg_range=gwg_range,
                                                weights={const_name1: [1]})

        pred_by_gwg_const_SGA = get_pred_by_gwg(predictor=Predictor(targets=[const_name2]),
                                                patient_features=patient_features,
                                                gwg_range=gwg_range,
                                                weights={const_name2: [1]})

        pred_by_gwg_const_LGA.rename(inplace=True, columns={"pred": const_name1})
        pred_by_gwg_const_SGA.rename(inplace=True, columns={"pred": const_name2})

        pred_by_gwg_const = pred_by_gwg_const_LGA.merge(pred_by_gwg_const_SGA, on="GWG")

        gwg_interval_recommendation = get_gwg_interval_recommendation_2T(pred_by_gwg=pred_by_gwg,
                                                                         pred_by_gwg_const=pred_by_gwg_const,
                                                                         const_name1=const_name1,
                                                                         const_name2=const_name2,
                                                                         gwg_limit=gwg_limit,
                                                                         pred_limit=pred_limit,
                                                                         const_th1=const_th1,
                                                                         const_th2=const_th2)
        recom_fmt = {}

        for k in gwg_interval_recommendation:
            recom_fmt["{}_GWG".format(k)] = gwg_interval_recommendation[k][0]
            recom_fmt["{}_score".format(k)] = gwg_interval_recommendation[k][1]

        gwg_interval_recommendations = gwg_interval_recommendations.append(recom_fmt,
                                                                           ignore_index=True)

    tf = time.time()
    df = timedelta(seconds=tf - ti)

    print("Total time {} to process {} obs".format(df, len(patients_features)))

    return gwg_interval_recommendations
