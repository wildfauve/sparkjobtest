from typing import Callable
from pyspark.sql import SparkSession
# from simple_memory_cache import GLOBAL_CACHE

from sparkjobtest.util import singleton

# spark_session_cache = GLOBAL_CACHE.MemoryCachedVar('spark_session_cache')

class SessionConfig(singleton.Singleton):

    def configure(self, spark_session, table_format: str="delta") -> None:
        self.spark_session = spark_session
        self.table_format = table_format
        pass

    def configured(self):
        return getattr(self, "spark_session", None)


def build(spark_session=None, table_format="delta"):
    if SessionConfig().configured():
        return
    SessionConfig().configure(spark_session if spark_session else create_session(), table_format)


def session():
    return SessionConfig().spark_session

def table_format():
    return SessionConfig().table_format

# def session():
#     return spark_session_cache.get()
#
# def invalidate_cache():
#     spark_session_cache.invalidate()
#     pass
#
# @spark_session_cache.on_first_access
def create_session():
    return SparkSession.builder.getOrCreate()