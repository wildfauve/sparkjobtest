import argparse
import sys
from pymonad.tools import curry
from pyspark.sql import dataframe
from uuid import uuid4

from sparkjobtest.model import manifest, graph, value
from sparkjobtest.util import session, monad, config, tracer, logger, env

loc = "{}/FileStore/cbor/batch/graph.json".format(config.dbfs)

def job(ids=None, location=None) -> monad.EitherMonad:
    session_builder()

    result = (build_value(location, ids, ",".join(sys.argv))
              >> start_manifest
              >> read_graph
              >> build_cbor
              >> transform
              >> write
              >> complete_manifest)

    logger.log(level='info',
               msg='Job End',
               status="ok" if result.is_right() else "fail",
               ctx={},
               tracer=result.lift().tracer)


    return result


def build_value(location, ids, args) -> monad.EitherMonad[value.JobState]:
    param_ids = ids if ids else "no_params"
    job_id = str(uuid4())
    trace = tracer.Tracer(env=env.Env.env, job_id=job_id)

    logger.log(level='info',
               msg='Job Start',
               ctx={'ids': param_ids, 'args': args},
               tracer=trace)

    return monad.Right(value.JobState(uuid=job_id,
                                      tracer=trace,
                                      params=value.JobParams(file_location=location if location else loc,
                                                             ids=param_ids,
                                                             args=args)))

def start_manifest(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = manifest.add_state(uuid=job_state.uuid, loc=job_state.params.file_location, state="initiated")
    if result.is_right():
        return monad.Right(job_state)
    return monad.Left(job_state.replace('error', result.error()))


def read_graph(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = graph.read_graph(job_state.params.file_location)
    if result.is_right():
        return monad.Right(job_state.replace('graph', result.value))
    return monad.Left(job_state.replace('error', result.error()))


def build_cbor(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = graph.build_cbor_df(job_state.graph)
    if result.is_right():
        return monad.Right(job_state.replace('df', result.value))
    return monad.Left(job_state.replace('error', result.error()))


def transform(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = graph.transform(df=job_state.df, params=job_state.params)
    if result.is_right():
        return monad.Right(job_state.replace('df', result.value))
    return monad.Left(job_state.replace('error', result.error()))


def write(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = graph.write(df=job_state.df)
    if result.is_right():
        return monad.Right(job_state)
    return monad.Left(job_state.replace('error', result.error()))

def complete_manifest(job_state: value.JobState) -> monad.EitherMonad[value.JobParams]:
    result = manifest.add_state(uuid=job_state.uuid, loc=job_state.params.file_location, state="complete")
    if result.is_right():
        return monad.Right(job_state)
    return monad.Left(job_state.replace('error', result.error()))

def session_builder():
    session.build(spark_session=None, table_format="delta")
