import numpy as np
import pandas as pd

from sklearn import metrics

__all__ = [
    "FEATURE_NAMES",

    "fires",

    "X",
    "y_raw",
    "y_log",
    "y_sin",

    "custom_scorer",
]


FEATURE_NAMES = [
    "DC",
    "temp",
    "RH",
    "wind",
]

fires = pd.read_csv("./forestfires.csv")

X = fires[FEATURE_NAMES]
y_raw = fires["area"]
y_log = fires["log(area+1)"]
y_sin = fires["sin(area)"]


#############################
## Root Mean Squared Error ##
#############################

custom_scorer = metrics.make_scorer(
    lambda y, y_pred: np.sqrt(metrics.mean_squared_error(y, y_pred)), greater_is_better=False
)
