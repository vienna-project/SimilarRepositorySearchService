FROM python:3.6

ARG embedding_path=./volume/embedding.h5
ENV num_tree=50

COPY service/ /home/service
COPY run.py /home/run.py

RUN pip install --upgrade pip
RUN pip install pandas==0.24 annoy==1.16 redis==3.4.0 "sanic>=20" gunicorn requests tables

COPY ${embedding_path} /home/volume/embedding.h5

WORKDIR /home/

ENTRYPOINT ["gunicorn", "run:app"]
CMD ["-b", "0.0.0.0:8000", "-k", "sanic.worker.GunicornWorker", "-t", "180"]