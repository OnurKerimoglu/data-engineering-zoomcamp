#Cleaned up version of data-loading.ipynb
import argparse
import logging 
import os, sys
import pandas as pd 
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from time import time

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
    )
logger = logging.getLogger(__name__)

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    tb = params.tb
    url = params.url
    
    logger.info(f'Connecting to {user}@{host}:{port}/{db}...')

    # Create SQL engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Get the name of the file from url
    file_name = url.rsplit('/', 1)[-1].strip()
    cwd = os.path.abspath(os.getcwd())
    fpath = os.path.join(cwd, 'data', file_name)

    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists(fpath):
        logger.info(f'Downloading {file_name} to {fpath} ...')
        # Download file from url
        os.system(f'curl {url.strip()} -o {fpath}')
        logger.info('Downloading finished.')
    else:
        logger.info(f'{file_name} already exists in {fpath}.')

    # Read file based on csv or parquet
    if '.csv' in fpath:
        df = pd.read_csv(fpath, nrows=10)
        df_iter = pd.read_csv(fpath, iterator=True, chunksize=100000)
    elif '.parquet' in fpath:
        file = pq.ParquetFile(fpath)
        df = next(file.iter_batches(batch_size=10)).to_pandas()
        df_iter = file.iter_batches(batch_size=100000)
    else: 
        logger.error('Error. Only .csv or .parquet files allowed.')
        sys.exit()


    # Create the table
    df.head(0).to_sql(name=tb, con=engine, if_exists='replace')


    # Insert values
    t_start = time()
    count = 0
    for batch in df_iter:
        count+=1

        if '.parquet' in file_name:
            batch_df = batch.to_pandas()
        else:
            batch_df = batch

        logger.info(f'inserting batch {count}...')

        b_start = time()
        batch_df.to_sql(name=tb, con=engine, if_exists='append')
        b_end = time()

        logger.info(f'inserted! time taken {b_end-b_start:10.3f} seconds.\n')
        
    t_end = time()   
    logger.info(f'Completed! Total time taken was {t_end-t_start:10.3f} seconds for {count} batches.')    



if __name__ == '__main__':
    #Parsing arguments 
    parser = argparse.ArgumentParser(description='Loading data from .paraquet file link to a Postgres datebase.')

    parser.add_argument('--user', help='Username for Postgres.')
    parser.add_argument('--password', help='Password to the username for Postgres.')
    parser.add_argument('--host', help='Hostname for Postgres.')
    parser.add_argument('--port', help='Port for Postgres connection.')
    parser.add_argument('--db', help='Databse name for Postgres')
    parser.add_argument('--tb', help='Destination table name for Postgres.')
    parser.add_argument('--url', help='URL for .paraquet file.')

    args = parser.parse_args()
    main(args)




