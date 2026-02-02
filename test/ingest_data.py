#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


def run(
    pg_user: str,
    pg_password: str,
    pg_host: str,
    pg_port: int,
    pg_db: str,
    year: int,
    month: int,
    target_table: str,
    chunksize: int,
):
    """
    Ingest taxi data for a given year/month into Postgres.
    """
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}yellow_tripdata_{year}-{month:02d}.csv.gz'

    engine = create_engine(
        f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'
    )

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )

    print("Ingestion completed successfully.")


@click.command()
@click.option('--pg-user', default='root', show_default=True, help='Postgres user')
@click.option('--pg-password', default='root', show_default=True, help='Postgres password')
@click.option('--pg-host', default='localhost', show_default=True, help='Postgres host')
@click.option('--pg-port', default=5432, type=int, show_default=True, help='Postgres port')
@click.option('--pg-db', default='ny_taxi', show_default=True, help='Postgres database')
@click.option('--year', default=2021, type=int, show_default=True, help='Year of the data')
@click.option('--month', default=1, type=click.IntRange(1, 12), show_default=True, help='Month of the data (1-12)')
@click.option('--target-table', default='yellow_taxi_data', show_default=True, help='Target table name')
@click.option('--chunksize', default=100000, type=int, show_default=True, help='Chunk size for ingestion')
def main(pg_user, pg_password, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    run(pg_user, pg_password, pg_host, pg_port, pg_db, year, month, target_table, chunksize)


if __name__ == '__main__':
    main()  # test/ingest_data.py