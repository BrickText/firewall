import numpy as np
import pandas as pd

from sklearn import metrics

__all__ = [
    "FEATURE_NAMES",

    "fires",
    "fires_classif",

    "custom_scorer",
]


FEATURE_NAMES = [
    "temp",
    "RH",
    "wind",
    "rain",
]

fires = pd.read_csv("../fires.csv")
fires_classif = pd.read_csv("../fires_classif.csv")

#############################
## Root Mean Squared Error ##
#############################

custom_scorer = metrics.make_scorer(
    lambda y, y_pred: np.sqrt(metrics.mean_squared_error(y, y_pred)), greater_is_better=False
)
