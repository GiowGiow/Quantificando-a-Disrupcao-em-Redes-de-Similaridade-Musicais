import pandas as pd

def plot_genre_distribution(df, most_popular=15):
    """ Plots the genre distribution of the most popular genres in the dataframe
    - Needs a genre column in the dataframe
    """
    
    # Join all the genres in a string and the split them
    genres = ",".join(df['genres']).split(",")
    
    # That way we can count the occurrences of all genres in the dataframe
    genres_series = pd.Series(genres)
    print(f"Number of unique genres in the dataset: {genres_series.nunique()}")
    
    genres_count = genres_series.value_counts()
    ax = genres_count[:most_popular].plot.bar(title="Distribuição de Gêneros no dataset")


# Deprecated
def find_empty_songs_export_dataset(df, similarity_matrix):
    """ Function to remove and export the dataset without the empty songs
        needs to be ran after the similarity matrix has been computed """
    def get_df_size(df):
        return np.shape(df)[0]
        
    def find_madonna_song_index(df):
        """ Finds a song that we know that doesn't have audio """
        return df.query("song == 'Candy Shop Medley (Live)'").index
    
    madonna_song_index = find_madonna_song_index(df)
    # the [0] its because it is a 2d array containing only 1 list
    madonna_row = similarity_matrix[madonna_song_index][0] 
    empty_samples_to_exclude_list = np.where(madonna_row > 0.9)[0]
    np.append(empty_samples_to_exclude_list, madonna_song_index)

    print(f"There are {len(empty_samples_to_exclude_list)} empty songs")

    # find their ids
    empty_samples_to_exclude_list_ids = df['id'][empty_samples_to_exclude_list].to_list()
    
    print("Removing empty songs from dataset")
    df = df[~df['id'].isin(empty_samples_to_exclude_list_ids)]
    
    print(f"Exporting dataset of size {get_df_size(df)}")
    df.to_csv(f"song_info_dataset_{get_df_size(df)}_entries_filtered.csv", index=False)


from math import ceil

"""
# Helper functions to help analyze/filter the dataset 
# Exploring a bit with the information we got
## Showing some songs with high similarity

### When using gamma = 0.01, only masters and remasters of the same songs show as similar
# get_songs_list(dataframe, similarity_matrix, 0.8)

beatles_df = dataframe.query("artist == 'The Beatles'")
print(len(beatles_df))
beatles_feature_vector = get_feature_vector(beatles_df)
beatles_similarity_matrix = rbf_kernel(beatles_feature_vector, gamma=0.001)
np.fill_diagonal(beatles_similarity_matrix, 0)
get_songs_list(beatles_df, beatles_similarity_matrix, 0.7)

"""

def show_similarity(df, similarity_matrix, song_index, song_two_index):
    """ Shows the similarity of two entries of a similarity matrix """
    print()
    print(df.iloc[song_index])
    print(df.iloc[song_two_index])
    print()
    similarity = similarity_matrix[song_index, song_two_index]
    print(f"Similarity: {similarity}")
    
def get_songs_list(df, similarity_matrix, similarity_threshold, limit=10):
    """ Get the list of song similarities for a similarity threshold """
    rows, columns = np.where(similarity_matrix > similarity_threshold)
    print(len(similarity_matrix[rows, columns]))
    songs_list = np.array((rows, columns)).T
    songs_list = songs_list[:ceil(len(songs_list)/2)]
    for song in songs_list[:limit]:
        show_similarity(df, similarity_matrix, song[0], song[1])



