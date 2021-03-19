from sklearn.metrics.pairwise import rbf_kernel
from scipy.spatial.distance import sqeuclidean
import numpy as np
import time
from tqdm import tqdm

X = [[1,2,3],
    [2 ,3,4],
    [0 ,1,2]]
gamma = 0.01

def load_features_from_file(path):
    with open(path, 'r') as features_file:
        return [[float(feature) for feature in feature_set.split()] for feature_set in features_file.readlines()]

start = time.time()

features_matrix = load_features_from_file(
    '../features/all_features-forro.txt'
    )

end = time.time()
print(f"Demorou {end - start}s para carregar")
print(f"Shape: ({len(features_matrix)},{len(features_matrix[0])})")

#start = time.time()
#A = rbf_kernel(features_matrix, gamma=gamma)
#end = time.time()
#print(f"Demorou {end - start}s para fazer a matriz...")


def rbf_kernel_manual(feature_mat, gamma):
    start = time.time()
    for i in tqdm(range(len(feature_mat))):
        for j in tqdm(range(len(feature_mat))):
            x = sqeuclidean(feature_mat[i], feature_mat[j]) 
    end = time.time()
    print(f"Demorou {end - start}s para fazer a matriz manualmente...")

rbf_kernel_manual(features_matrix, gamma=0.01)