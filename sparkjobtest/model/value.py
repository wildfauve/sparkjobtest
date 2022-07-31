from typing import Dict
from dataclasses import dataclass
from pyspark.sql import dataframe

@dataclass
class DataClassAbstract:
    def replace(self, key, value):
        setattr(self, key, value)
        return self

@dataclass
class JobParams(DataClassAbstract):
    file_location: str
    ids: str
    args: str


@dataclass
class JobState(DataClassAbstract):
    uuid: str
    params: JobParams
    graph_df: dataframe.DataFrame = None
    manifest_df: dataframe.DataFrame = None


