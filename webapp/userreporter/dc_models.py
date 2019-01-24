import pickle


with open('../models/fire_area.b', 'rb') as f:
    FIRE_AREA = pickle.load(f)

with open('../models/fire_clustering_200.b', 'rb') as f:
    FIRE_CLUSTERING = pickle.load(f)

with open('../models/fire_proba.b', 'rb') as f:
    FIRE_PROBA = pickle.load(f)
