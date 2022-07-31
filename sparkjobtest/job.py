import argparse
import sys
from pymonad.tools import curry
from pyspark.sql import dataframe
from uuid import uuid4

from sparkjobtest.model import manifest, graph, value
from sparkjobtest.util import session, monad, config

loc = "{}/FileStore/cbor/batch/graph.json".format(config.dbfs)

def job(ids=None, location=None) -> monad.EitherMonad:
    session_builder()

    result = (build_value(location, ids, ",".join(sys.argv))
              >> start_manifest
              >> read_file
              >> transform
              >> write
              >> complete_manifest)
    return result


def build_value(location, ids, args) -> monad.EitherMonad[value.JobState]:
    (ids if ids else "no_params", ",".join(sys.argv))
    return monad.Right(value.JobState(uuid=str(uuid4()),
                                      params=value.JobParams(file_location=location if location else loc,
                                                             ids=ids if ids else "no_params",
                                                             args=args)))

def start_manifest(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = manifest.add_state(uuid=job_state.uuid, loc=job_state.params.file_location, state="initiated")
    return monad.Right(job_state)


def read_file(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = graph.read_graph(job_state.params.file_location)
    return monad.Right(job_state.replace('graph_df', result))


def transform(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = graph.transform(df=job_state.graph_df, params=job_state.params)
    return monad.Right(job_state.replace('graph_df', result))


def write(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = graph.write(df=job_state.graph_df)
    return monad.Right(job_state)

def complete_manifest(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = manifest.add_state(uuid=job_state.uuid, loc=job_state.params.file_location, state="complete")
    return monad.Right(job_state)

def session_builder():
    session.build(spark_session=None, table_format="delta")
