from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from delta.tables import *

import pendulum

from sparkjobtest.util import session as sp
from sparkjobtest.util import config

db = "dataProduct_cbor"
tablename = "job_manifest"
job_manifest = "dataProduct_cbor.job_manifest"

schema = StructType([
    StructField('uuid', StringType(), True),
    StructField('batch', StringType(), True),
    StructField('processState', StringType(), True),
    StructField('stateChangeTime', StringType(), True)
])


def add_state(uuid: str, loc: str, state: str) -> bool:
    # tbl = create_table_if_not_exist(session().createDataFrame([], schema))
    df = create_df(uuid, loc, state)
    upsert(df)
    return True

def create_df(uuid, loc, state):
    return session().createDataFrame([(uuid, loc, state, pendulum.now().to_iso8601_string())], schema)

def create_table(df):
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

def upsert(upd):
    # if delta_table_format():
    #     (man.alias('m')
    #         .merge(upd.alias('u'), 'm.batch = u.batch')
    #         .whenNotMatchedInsert(values={"batch": "u.batch", "processState": "u.processState", "stateChangeTime": "u.stateChangeTime"})
    #         .execute())
    # else:
    upd.write.format(sp.table_format()).mode("append").saveAsTable(config.manifest_table_fully_qualified)
    return True


def session():
    return sp.session()

def delta_table_format():
    return sp.table_format() == "delta"