#!/bin/bash

find /songs -type f ! -name '*.txt' ! -name "*.npy" > songs_list.txt

/bin/python easy_feature_extraction.py /songs/songs_list.txt /songs/features.npy 8