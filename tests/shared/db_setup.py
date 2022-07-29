import pytest

from pathlib import Path
import shutil
import pyspark

from delta import *


@pytest.fixture
def init_db():
    from sparkjobtest.util import session
    session.session().sql("drop database IF EXISTS dataProduct_cbor CASCADE")
    # dirpath = Path('spark-warehouse')
    # if dirpath.exists() and dirpath.is_dir():
    #     shutil.rmtree(dirpath)
    session.session().sql("create database IF NOT EXISTS dataProduct_cbor")
    # builder = (pyspark.sql.SparkSession.builder.appName("MyApp")
    #            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    #            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
    # breakpoint()
