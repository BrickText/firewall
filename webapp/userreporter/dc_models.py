import pickle

# from userreporter.stacked_model import StackedModel


with open('../models/fire_clustering_100.b', 'rb') as f:
    FIRE_CLUSTERING = pickle.load(f)

with open('../models/fire_area.b', 'rb') as f:
    FIRE_AREA = pickle.load(f)

with open('../models/fire_proba.b', 'rb') as f:
    FIRE_PROBA = pickle.load(f)
