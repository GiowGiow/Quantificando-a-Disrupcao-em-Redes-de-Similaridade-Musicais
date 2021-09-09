FROM python:2.7

RUN apt update && apt-get install -y \
    git \
    libsndfile1-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
    
# Download specific library versions as python 2 was deprecated and thus became
# increasingly hard for pip to download the correct python 2 package.
# RUN pip install llvmlite==0.27 numba==0.42 pandas==0.22 librosa==0.7 theano==0.9 keras==1.2.2 tensorflow==1.15.0
RUN pip install llvmlite==0.27 numba==0.42 pandas==0.22 librosa==0.7 theano==0.9 keras==1.2.2 tensorflow==1.15.0 ffmpeg

# Download repositories
RUN git clone https://github.com/keunwoochoi/kapre.git
RUN cd kapre && git checkout a3bde3e && python setup.py install

COPY ./requirements.txt /
RUN pip install -r requirements.txt

RUN git clone https://github.com/keunwoochoi/transfer_learning_music
# Set Run permissions
RUN chmod +x transfer_learning_music/easy_feature_extraction.py

RUN mkdir songs
RUN mkdir ~/.keras

# From https://github.com/keunwoochoi/transfer_learning_music:
# set image_dim_ordering : th in ~/keras/keras.json
# set backend : theano, too.
# I'm just copying my own .json here
COPY ./keras.json /root/.keras/keras.json

WORKDIR /transfer_learning_music

COPY start.sh .
RUN chmod +x start.sh

ENTRYPOINT [ "start.sh" ]