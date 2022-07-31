from pyspark.sql.functions import lit
from pyspark.sql import dataframe
import pendulum

from sparkjobtest.util import session as sp
from sparkjobtest.util import config
from sparkjobtest.model import value

ftype = "csv"

def transform(df: dataframe.DataFrame, params: value.JobParams):
    lib_test = "dbutils: {} Spark: {}".format("dbutils" in locals(), "spark" in locals())
    return (df.withColumn("_loadtime", lit(pendulum.now("Europe/Paris")))
              .withColumn("_params", lit(params.ids))
              .withColumn("_args", lit(str(params.args)))
              .withColumn("_libs", lit(lib_test)))

def write(df: dataframe.DataFrame):
    df.show()
    df.write.format(sp.table_format()).mode("append").saveAsTable(config.batch_table_fully_qualified)
    return True


def read_csv(location):
    infer_schema = "true"
    first_row_is_header = "true"
    delimiter = ","

    df = session().read.format(ftype) \
      .option("inferSchema", infer_schema) \
      .option("header", first_row_is_header) \
      .option("sep", delimiter) \
      .load(location)

    df.show()

    return df

def session():
    return sp.session()
