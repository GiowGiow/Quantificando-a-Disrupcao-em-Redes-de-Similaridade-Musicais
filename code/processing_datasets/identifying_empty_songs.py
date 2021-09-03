########## Description ##############
# A simple script to identify silent songs and export a list of the ids that are empty
# It needs sox and tqdm to run 

#####################################
# The sox lib can identify the maximum amplitude of a MP3
# The second package is the MP3 handler for the sox library
# !sudo apt install sox libsox-fmt-mp3
# !pip install sox

import sox
from tqdm import tqdm
from pathlib import Path

DATASET_PATH = Path("../../../dataset/music4all/")

mp3_ids = []
mp3_path = DATASET_PATH / "audios"
print(mp3_path)
all_mp3_songs = list(mp3_path.glob("*.mp3"))
print(len(all_mp3_songs))

for song in tqdm(all_mp3_songs):
    if sox.file_info.silent(str(song)):
        print(f"song with id: {str(song)} is empty!")
        mp3_ids.append(song.stem)
        

with open("empty_mp3_ids.txt", "w") as file:
    for song_id in mp3_ids:
        file.write(song_id + "\n")