import argparse
import sys

from sparkjobtest.model import manifest, batch
from sparkjobtest.util import session

loc = "/FileStore/cbor/batch/test.csv"

def job(ids=None, location=None):
    session_builder()

    file_location = location if location else loc

    batch.write(batch.transform(df=batch.read_csv(file_location), params=ids if ids else "no_params", args= ",".join(sys.argv)))
    # update_manifest(file_location)
    return True


def update_manifest(file_location):
    return manifest.new_manifest(file_location, "complete")


def session_builder():
    session.build(spark_session=None, table_format="delta")