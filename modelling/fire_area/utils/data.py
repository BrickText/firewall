import numpy as np
import pandas as pd

__all__ = [
    "FEATURE_NAMES",
    "fires",
]


FEATURE_NAMES = [
    "temp",
    "RH",
    "wind",
    "rain",
]

fires = pd.read_csv("../fires.csv")
