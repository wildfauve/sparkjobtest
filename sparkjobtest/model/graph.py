from typing import Tuple, List
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import lit
from pyspark.sql import dataframe
import pendulum
from rdflib import Namespace, Graph, Literal, RDF
from pymonad.tools import curry

from sparkjobtest.util import session as sp
from sparkjobtest.util import config, fn
from sparkjobtest.model import value, cbor_schema
from sparkjobtest.ontology import rdf_prefix as P
from sparkjobtest.ontology import bindings

def transform(df: dataframe.DataFrame, params: value.JobParams):
    lib_test = "dbutils: {} Spark: {}".format("dbutils" in locals(), "spark" in locals())
    return (df.withColumn("_loadtime", lit(pendulum.now("Europe/Paris")))
            .withColumn("_params", lit(params.ids))
            .withColumn("_args", lit(str(params.args)))
            .withColumn("_libs", lit(lib_test)))


def write(df: dataframe.DataFrame):
    df.show()
    df.write.format(sp.table_format()).mode("append").saveAsTable(config.graph_table_fully_qualified)
    return True


def read_graph(location):
    g = init_graph(location)
    rows = [build_portfolio_constituent(g, portfolio_triple, constituent_triple) for portfolio_triple in portfolios(g)
            for constituent_triple in constituents(g, portfolio_triple)]
    return session().createDataFrame(rows, cbor_schema.schema)


def build_portfolio_constituent(g, portfolio: Tuple, constituent: Tuple):
    s, _, o = portfolio
    _, _, tag = first_matching_triple(g, (s, P.lcc_lr.hasTag, None))
    built_position = position(g, constituent)
    return (
        (str(s), str(o), tag.value), # portfolio type_id_tag
        built_position
    )

def position(g, constituent: Tuple) -> Tuple[str, str]:
    _, p, o = constituent
    constituent_props = all_matching_triples(g, (o, None, None))
    _, _, position_valuation_change = triple_finder(P.sfo_prt.hasPositionValuationChange, constituent_props)
    return (str(o), str(p))


def init_graph(location):
    g = Graph()

    bindings.bind(g)
    g.parse(location)
    return g


def portfolios(g) -> List:
    return g.triples((None, RDF.type, P.fibo_sec_fund_civ.FundPortfolio))


def constituents(g, portfolio_triple) -> List:
    return g.triples((portfolio_triple[0], P.fibo_fnd_arr_arr.hasConstituent, None))

#
# Helpers
#
@curry(2)
def cond_predicate(term, triple: Tuple) -> bool:
    return triple[1] == term


def triple_finder(term, t_map: List[Tuple], filter_fn=fn.find, cond=cond_predicate):
    """
    Takes a triples map and applies a filter fn and a condition to return either
    a List[(s,p,o)] or (s,p,o)
    """
    result = filter_fn(cond(term), t_map)
    if result:
        return result
    return (None, None, None)


def first_matching_triple(g, pattern: Tuple) -> Tuple:
    return list(g.triples(pattern))[0]

def all_matching_triples(g, pattern: Tuple) -> List[Tuple]:
    return list(g.triples(pattern))

def session():
    return sp.session()
