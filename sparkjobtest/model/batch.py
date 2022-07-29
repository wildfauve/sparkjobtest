from pyspark.sql.functions import lit
import pendulum

from sparkjobtest.util import session as sp

ftype = "csv"

def transform(df, params, args):
    lib_test = "dbutils: {} Spark: {}".format("dbutils" in locals(), "spark" in locals())
    return (df.withColumn("_loadtime", lit(pendulum.now("Europe/Paris")))
              .withColumn("_params", lit(params))
              .withColumn("_args", lit(str(args)))
              .withColumn("_libs", lit(lib_test)))

def write(df):
    df.write.format(sp.table_format()).mode("overwrite").saveAsTable("dataProduct_cbor.batch")
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
