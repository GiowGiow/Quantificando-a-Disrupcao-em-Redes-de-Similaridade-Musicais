from sklearn.metrics.pairwise import rbf_kernel
from scipy.spatial.distance import sqeuclidean
import numpy as np
import time

X = [[1,2,3],
    [2 ,3,4],
    [0 ,1,2]]

gamma = 0.01

def load_features_from_file(path):
    with open(path, 'r') as features_file:
        return [[float(feature) for feature in feature_set.split()] for feature_set in features_file.readlines()]

start = time.time()
features_matrix = load_features_from_file(
    '/home/giovanni-server/dev/college/TCC/features/all_features-forro.txt'
    )
end = time.time()

print(f"Demorou {end - start}s para carregar")
print(f"Shape: ({len(features_matrix)},{len(features_matrix[0])})")
print(len(features_matrix), len(features_matrix[0]))

start = time.time()
similarity_matrix = rbf_kernel(features_matrix, gamma=gamma)
end = time.time()

print(f"Demorou {end - start}s para fazer a matriz...")