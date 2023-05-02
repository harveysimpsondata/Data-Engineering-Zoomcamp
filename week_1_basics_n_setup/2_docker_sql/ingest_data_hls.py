import os
import argparse
import pandas as pd
from sqlalchemy import create_engine


def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table_name = params.table_name
    url = params.url

    #download the parquet file

    parquet_name = 'output.parquet'

    os.system(f'wget {url} -O {parquet_name}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    #engine.connect()

    df = pd.read_parquet(parquet_name, engine='auto')

    def upload_df_to_sql(df, table_name, engine, chunksize):
        """
        Upload a DataFrame to an SQL database in chunks.

        :param df: The DataFrame to upload
        :param table_name: The name of the table in the database
        :param engine: An SQLAlchemy engine connected to the database
        :param chunksize: The size of each chunk
        """
        # Split the DataFrame into chunks
        chunks = [df[i:i + chunksize] for i in range(0, df.shape[0], chunksize)]

        # Upload each chunk to the database
        for i, chunk in enumerate(chunks, start=1):
            print(f'Uploading chunk {i}/{len(chunks)}')
            chunk.to_sql(
                name=table_name,
                con=engine,
                if_exists='append',  # Add data to the table if it exists
                index=False,  # Don't write the index column
            )
            print(f'Chunk {i}/{len(chunks)} uploaded')

    upload_df_to_sql(df, table_name, engine, 100000)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest parquet data into Postgres")

    parser.add_argument('--user', type=str, help='user name for postgres')
    parser.add_argument('--password', type=str, help='password for postgres')
    parser.add_argument('--host', type=str, help='host for postgres')
    parser.add_argument('--port', type=str, help='port for postgres')
    parser.add_argument('--database', type=str, help='database name for postgres')
    parser.add_argument('--table_name', type=str, help='table name where we will write our results to')
    parser.add_argument('--url', type=str, help='url of the parquet file')

    args = parser.parse_args()

    main(args)


