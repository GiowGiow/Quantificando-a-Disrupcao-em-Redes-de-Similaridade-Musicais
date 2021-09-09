# Extracting Features

To extract MFCC features the notebook has a fairly comprehensible take on extracting the MFCC features for the current dataset

## Convnet Features

To facilitate the dependency problems an image was build to fully extract features.
A volume mapping with the songs is needed to be passed to the container so it can extract the representation vector for each song.

To build the image:

`docker build . -t feature_extractor`

To extract the features:

`docker run -it -v <folder_with_songs>:/songs feature_extractor`