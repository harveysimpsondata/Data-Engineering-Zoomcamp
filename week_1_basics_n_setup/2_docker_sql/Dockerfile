FROM python:3.9.1

RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean
RUN pip install pandas sqlalchemy psycopg2 pyarrow

WORKDIR /app
COPY ingest_data_hls.py ingest_data_hls.py

ENTRYPOINT [ "python", "ingest_data_hls.py" ]