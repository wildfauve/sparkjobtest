import argparse
import sys
from pymonad.tools import curry
from pyspark.sql import dataframe

from sparkjobtest.model import manifest, batch
from sparkjobtest.util import session, monad

loc = "/FileStore/cbor/batch/test.csv"

def job(ids=None, location=None) -> monad.EitherMonad:
    session_builder()

    file_location = location if location else loc


    result = read_file(file_location) >> transform(ids if ids else "no_params", ",".join(sys.argv)) >> write
    # update_manifest(file_location)
    return result


def read_file(file_location) -> monad.EitherMonad[dataframe.DataFrame]:
    result = batch.read_csv(file_location)
    return monad.Right(result)


@curry(3)
def transform(params, args, df) -> monad.EitherMonad[dataframe.DataFrame]:
    result = batch.transform(df=df, params=params, args=args)
    return monad.Right(result)


def write(df) -> monad.EitherMonad[dataframe.DataFrame]:
    result = batch.write(df=df)
    return monad.Right(result)

def update_manifest(file_location):
    return manifest.new_manifest(file_location, "complete")


def session_builder():
    session.build(spark_session=None, table_format="delta")