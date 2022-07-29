from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from delta.tables import *

import pendulum

from sparkjobtest.util import session as sp

db = "dataProduct_cbor"
tablename = "job_manifest"
job_manifest = "dataProduct_cbor.job_manifest"

schema = StructType([
    StructField('batch', StringType(), True),
    StructField('processState', StringType(), True),
    StructField('stateChangeTime', StringType(), True)
])


def new_manifest(loc, state):
    tbl = create_table_if_not_exist(session().createDataFrame([], schema))
    breakpoint()
    df = create_df(loc, state)
    upsert(tbl, df)
    return True

def create_df(loc, state):
    return session().createDataFrame([(loc, state, pendulum.now().to_iso8601_string())], schema)

def create_table(df):
    breakpoint()
    df.write.mode("overwrite").format("delta").saveAsTable(job_manifest)

def create_table_if_not_exist(empty_df):
    if not test_table_exists(job_manifest):
        create_table(empty_df)
    return table()

def test_table_exists(table):
    if "3.3" in session().version:
        return session().catalog.tableExists(table)
    return tablename in list(map(lambda t: t.name, session().catalog.listTables(db)))

def table():
    return DeltaTable.forName(session(), job_manifest)
    # return spark.table(job_manifest)

def upsert(man, upd):
    (man.alias('m')
        .merge(upd.alias('u'), 'm.batch = u.batch')
        .whenNotMatchedInsert(values={"batch": "u.batch", "processState": "u.processState", "stateChangeTime": "u.stateChangeTime"})
        .execute())


def session():
    return sp.session()