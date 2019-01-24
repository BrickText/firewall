import numpy as np

__all__ = [
    "StackedModel",
]


class StackedModel:
    def __init__(self, *models):
        self.models = models

    def predict_log(self, X):
        return np.array([model.predict(X) for model in self.models]).mean(axis=0)

    def predict_raw(self, X):
        return np.exp(self.predict_log(X)) - 1
