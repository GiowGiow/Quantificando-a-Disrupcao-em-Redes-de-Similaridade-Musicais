import os
import numpy as np
import pandas as pd
import librosa
import time
from joblib import Parallel, delayed
from pathlib import Path
import logging
import warnings

# Ignore warnings from librosa
warnings.filterwarnings('ignore')

# Set logging profile
logging.basicConfig(filename='extract_features.log', level=logging.INFO)

# Set default folder structure
DATASET_PATH = "music4all/"
DATASET_PATH_AUDIOS = DATASET_PATH + "audios/"
FEATURE_FOLDER = 'dataset_mfcc/'

# Number of processes will be the number of cores available
n_proc = 8

# Dataset audio spec definition
SR = 22050 # [Hz] of the songs in Music4All dataset
len_src = 30. # [second]
ref_n_src = SR * len_src

if not os.path.exists(FEATURE_FOLDER):
    os.mkdir(FEATURE_FOLDER)

def gen_filepaths(df):
    """ Generate file path (column name 'filepath') from given dataframe """
    for file_name in df['id']:
        yield Path(DATASET_PATH_AUDIOS) / file_name + ".mp3"

def open_dataset(path):
    return pd.read_csv(path, sep='\t')

# Get mfcc given a dataframe.csv, look for every .mp3 file and extract a
# Feature vector based on the mfccs
def get_mfcc(filename):    
    start = time.time()
    csv_filename = '{}.csv'.format(filename)
    csv_path = Path(DATASET_PATH) / csv_filename
    
    df = open_dataset(csv_path)
    
    # Print some information abouth the dataset
    print('{}: Dataframe with size:{}'.format(filename, len(df)))
    
    # Check if some audio exists
    some_audio_file_name = df["id"][0] + ".mp3"
    some_audio_path = Path(DATASET_PATH_AUDIOS) / some_audio_file_name
    print(f"The file {some_audio_file_name} exists? {some_audio_path.exists()}")
    print(f"Number of Columns: {df.columns}")
    
    # Generate file paths
    gen_f = gen_filepaths(df)
    # Instantiate the lazy generated file paths
    paths = list(gen_f)
    
    # Number of paths to extract features
    print(len(paths))
    
    # Compute the 20 MFCCs with is delta and delta delta derivatives, with their mean and std dev.
    Parallel(n_jobs=n_proc, backend='multiprocessing')(delayed(compute_and_save_mfcc_from_path)(path) for path in paths)
    
    print('MFCC is done! in {:6.4f} sec'.format(time.time() - start))

def compute_and_save_mfcc_from_path(path):
    print("Song " + path)
    logging.info("Loading Song: " + path)
    try:
        src_zeros = np.zeros(1024) # min length to have 3-frame mfcc's
        src, sr = librosa.load(path, sr=SR, duration=30.) # max len: 30s, can be shorter.
        
        if len(src) < 1024:
            src_zeros[:len(src)] = src
            src = src_zeros

        # Compute the 20 MFCCs for the music in path
        logging.info("Computing MFCCs for: " + path)
        mfcc = librosa.feature.mfcc(src, SR, n_mfcc=20)
        
        # Remove the first and last frames as they do not contain information
        dmfcc = mfcc[:, 1:] - mfcc[:, :-1]  # delta derivative of the mfcc
        ddmfcc = dmfcc[:, 1:] - dmfcc[:, :-1] # delta delta derivative of the mfcc
        
        
        # Compute the feature array with the mean and standard
        # deviations of the computed MFCCs (and their derivatives)
        feats = np.array(np.concatenate((
                            np.mean(mfcc, axis=1), np.std(mfcc, axis=1),
                            np.mean(dmfcc, axis=1), np.std(dmfcc, axis=1),
                            np.mean(ddmfcc, axis=1), np.std(ddmfcc, axis=1))
                            , axis=0))

        
        # Saving the feature vector
        logging.info("Saving MFCCs: " + path)
        song_id = Path(path).stem
        np.save(os.path.join(FEATURE_FOLDER, f"{song_id}_mfcc.npy"), feats)

    except Exception as e:
        logging.error(f'Error occurred!: {e}')
        return

get_mfcc("id_metadata")