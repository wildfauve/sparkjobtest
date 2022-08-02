from typing import Dict, Optional, Any
from dataclasses import dataclass
from pyspark.sql import dataframe
from rdflib import Graph

from sparkjobtest.util import tracer

@dataclass
class DataClassAbstract:
    def replace(self, key, value):
        setattr(self, key, value)
        return self

@dataclass
class JobParams(DataClassAbstract):
    args: str

@dataclass
class JobState(DataClassAbstract):
    uuid: str
    tracer: tracer.Tracer
    params: JobParams
    graph: Graph = None
    df: Optional[dataframe.DataFrame] = None
    manifest_df: Optional[dataframe.DataFrame] = None
    error: Optional[Any] = None


