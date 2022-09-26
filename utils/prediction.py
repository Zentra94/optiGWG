import pickle
from pathlib import Path
import os

MAIN_PATH = Path(os.path.dirname(__file__)).parent


def load_models_from_targets(targets):
    models = {}
    for target in targets:
        path = MAIN_PATH / "data/models/{}/best_model.pkl".format(target)
        with open(path, "rb") as of:
            model = pickle.load(of)
        models[target] = model

    return models


def load_features_names_from_targets(targets):
    features_names = {}
    for target in targets:
        path = MAIN_PATH / "data/models/{}/numeric_features_names.pkl".format(target)
        with open(path, "rb") as of:
            numeric_feat = pickle.load(of)
        path = MAIN_PATH / "data/models/{}/categoric_features_names.pkl".format(target)
        with open(path, "rb") as of:
            categoric_feat = pickle.load(of)
        features_names[target] = numeric_feat + categoric_feat

    return features_names


class Predictor:
    def __init__(self, targets=None):
        if targets is None:
            targets = ["diabetes", "hipertension", "LGA", "SGA"]
        self.targets = targets
        self.models = load_models_from_targets(self.targets)
        self.features_names = load_features_names_from_targets(self.targets)

    def predict(self, X, target_name):
        model = self.models[target_name]
        features = self.features_names[target_name]
        return model.predict_proba(X=X[features])[:, 1]

    def preprocess(self, X, target_name):
        # TODO: WIP
        X_ = X.copy()
        return X_

    def predict_from_scratch(self, X, target_name):
        # TODO: WIP
        X_ = self.preprocess(X=X, target_name=target_name)
        return self.predict(X=X_, target_name=target_name)
