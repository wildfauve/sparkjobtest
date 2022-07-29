import pytest
from pyspark.sql import SparkSession


@pytest.fixture
def create_testing_pyspark_session():
    from sparkjobtest.util import session
    session.build(spark_session=test_session(), table_format="hive")

def test_session():
    return (SparkSession.builder
            .master('local[*]')
            .appName('test-pyspark-context')
            .enableHiveSupport()
            .getOrCreate())
