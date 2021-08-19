FROM lefant/python3-keras
WORKDIR /usr/app/notebooks
VOLUME /usr/app/

RUN pip install tensorflow==1.8.0
COPY notebooks/ /usr/app/notebooks

CMD jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --NotebookApp.allow_origin='*'
EXPOSE 8888