import networkx as nx
import pandas as pd
import numpy as np
import collections

from tqdm import tqdm
from networkx.drawing.nx_pylab import draw_networkx


def generate_network(list_of_songs, similarity_matrix, similarity_threshold=0.80):
    """ Generate a disruption network based on: 
    If a song has a similarity with another over the threshold than an edge is made to connect both of them.

    Args:
        1. list of songs (in the same order as the similarity matrix)
        2. A similarity matrix (ordered by release) so we know that the next song i + 1 is a song released after i
        3. A similarity threshold that will determine if there is an edge between nodes
    Returns:
        A network as a networkx.DiGraph Object
    """
    slice_index = 0
    G = nx.DiGraph()

    for i in tqdm(range(len(list_of_songs))):
        edge_count = 0
        
        G.add_node(i)
        
        for j in range(i + 1, len(list_of_songs)):
            # If there is a high similarity, create an edge between the nodes
            if similarity_matrix[i][j] > similarity_threshold:
                G.add_edge(j, i)
                edge_count += 1
        
        # If this node does not have a similarity with any other node, then remove the node
        if edge_count < 1:
            G.remove_node(i)

    return G

def get_disruption_index_for_nodes(list_of_songs, graph):
    """ Compute the actual disruption indexes for the graph based on the nodes(songs) and its
    connections (if its influenced or if it influenced another song) """
    disruption_info = {}

    for i in tqdm(range(len(list_of_songs))):    
        if graph.has_node(i):
            songs_after = range(i + 1, len(list_of_songs))
            song_influences = [edge[1] for edge in graph.edges(i) if edge[1] != i]

            ni = 0
            nj = 0
            nk = 0
            
            for song_after in songs_after:
                consolidating_influence = False
                if graph.has_edge(song_after , i):
                
                    for influence in song_influences:
                        if graph.has_edge(song_after, influence):
                            consolidating_influence = True
                            break
                
                    if consolidating_influence:
                        nj += 1
                    else:
                        ni += 1
                
                else:
                    for influence in song_influences:
                        if graph.has_edge(song_after, influence):
                            nk += 1
    
            disruption_info[list_of_songs.iloc[i]['id']] = [ni, nj, nk, float((ni-nj)) / float((ni+nj+nk))] if (ni + nj + nk) > 0 else [ni, nj, nk, 0]
    
    return disruption_info


from pathlib import Path

DATASET_PATH = Path("./dataset")

def load_npy(file_path):
    print(f"Loading: {file_path} ...")
    return np.load(file_path)

def load_features_from_file(file_name, feature_type):
    if feature_type == "mfcc":
        return load_npy(DATASET_PATH / "input" / "feature_vectors" / "mfcc" / file_name)
    elif feature_type == "transfer_learning":
        return load_npy(DATASET_PATH / "input" / "feature_vectors" / "transfer_learning" / file_name)
    else:
        raise TypeError("This feature type is not supported")

def load_similarity_matrix(file_name, feature_type):
    if feature_type == "mfcc":
        return load_npy(DATASET_PATH / "input" / "similarity_matrices" / "mfcc" / file_name)
    elif feature_type == "transfer_learning":
        return load_npy(DATASET_PATH / "input" / "similarity_matrices" / "transfer_learning" / file_name)
    else:
        raise TypeError("This feature type is not supported")

def load_dataframe(dataframe_file):
    print("Loading dataframe...")
    return pd.read_csv(DATASET_PATH / "input" / "csvs" / dataframe_file)

feat_type = "transfer_learning"
datset_size = 30000
gamma = 0.1

DF_PATH = f"sorted_song_info_{datset_size}.csv"
FEATS_PATH = f"{feat_type}_feature_vector_{datset_size}_samples.npy"
SIMILARITY_MATRIX_PATH = f"{feat_type}_{datset_size}_samples_{gamma}_gamma.npy"

dataframe = load_dataframe(DF_PATH)
features = load_features_from_file(FEATS_PATH, feat_type)
similarity_matrix = load_similarity_matrix(SIMILARITY_MATRIX_PATH, feat_type)

print("Generating Network...")
graph = generate_network(dataframe, similarity_matrix)

print("Calculating Disruption Index...")
disruption_index = get_disruption_index_for_nodes(dataframe, graph)

print("Saving Generated Graph...")
print(f"{feat_type}_{len(disruption_index)}_{gamma}")
nx.write_gexf(graph, DATASET_PATH / "output" / "graphs" / f"{feat_type}_{len(disruption_index)}_{gamma}.gexf")

import pickle

print("Saving Disruption Index...")
# Store data (serialize)
with open(DATASET_PATH / "output" / "disruption_index" / f'{feat_type}_{len(disruption_index)}_{gamma}.pickle', 'wb') as handle:
    pickle.dump(disruption_index, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("Merging disruption info with dataframe...")
disruption_index_df = pd.DataFrame(disruption_index).T
disruption_index_df.reset_index(inplace=True)
disruption_index_df.columns = ['id', 'ni', 'nj', 'nk', 'disruption']

song_info_with_disruption = pd.merge(disruption_index_df, dataframe, on='id')
print(f"New dataframe has {len(song_info_with_disruption)}")

print("Saving Dataframe with disruption information...")
song_info_with_disruption.to_csv(DATASET_PATH / "output" / "csv_with_disruption" / f"song_info_with_disruption_{len(song_info_with_disruption)}_feat_{feat_type}_gamma_{gamma}.csv", index=False)

print("All done!")