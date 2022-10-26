import pandas as pd
import matplotlib.pyplot as plt


def get_pred_by_gwg(predictor, patient_features, gwg_range, weights):
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

    plt.subplots(figsize=(10, 8))
    plt.plot(pred_by_gwg["GWG"], pred_by_gwg["pred"])
    plt.plot(interval_recommendation["best_gwg"][0], interval_recommendation["best_gwg"][1],
             c="r", marker='o', markeredgecolor="red", label="best GWG")
    plt.axvline(x=interval_recommendation["min_gwg"][0], color='r', label='min GWG',
                linestyle="dashed", linewidth=1, alpha=0.8)
    plt.axvline(x=interval_recommendation["max_gwg"][0], color='r', label='max GWG',
                linestyle="dashed", linewidth=1, alpha=0.8)

    plt.grid(True)
    plt.title(title)
    plt.savefig(path)


def get_gwg_interval_recommendation(gwg_limit, pred_limit, pred_by_gwg):
    best_idx = pred_by_gwg["pred"].idxmin()
    best_gwg = pred_by_gwg.loc[best_idx, "GWG"]
    best_pred = pred_by_gwg.loc[best_idx, "pred"]

    min_idx = best_idx
    min_gwg = best_gwg
    min_pred = best_pred

    while min_idx in pred_by_gwg.index and abs(min_gwg - best_gwg) < gwg_limit and abs(
            min_pred - best_pred) < pred_limit:
        min_idx += -1
        min_gwg = pred_by_gwg.loc[min_idx, "GWG"]
        min_pred = pred_by_gwg.loc[min_idx, "pred"]

    max_idx = best_idx
    max_gwg = best_gwg
    max_pred = best_pred

    while max_idx in pred_by_gwg.index and abs(max_gwg - best_gwg) < gwg_limit and abs(
            max_pred - best_pred) < pred_limit:
        max_idx += +1
        max_gwg = pred_by_gwg.loc[max_idx, "GWG"]
        max_pred = pred_by_gwg.loc[max_idx, "pred"]

    return {"min_gwg": (min_gwg, min_pred), "max_gwg": (max_gwg, max_pred), "best_gwg": (best_gwg, best_pred)}
