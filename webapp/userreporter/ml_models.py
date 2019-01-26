import pickle


with open('../bin/fire_area.b', 'rb') as f:
    FIRE_AREA = pickle.load(f)

with open('../bin/fire_clustering_150.b', 'rb') as f:
    FIRE_CLUSTERING = pickle.load(f)

with open('../bin/fire_proba.b', 'rb') as f:
    FIRE_PROBA = pickle.load(f)
