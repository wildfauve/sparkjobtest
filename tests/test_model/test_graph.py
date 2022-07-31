from sparkjobtest.util import session
from sparkjobtest.model import graph
# from tests.shared import graph

def setup_module():
    pass


def test_build_df_from_graph(create_testing_pyspark_session,
                             init_db):
    df = graph.read_graph(location="tests/fixtures/generated_graph.json")

    portfolio_rows = [d[0] for d in df.select(df.Portfolio).collect()]

    assert len(portfolio_rows) == 1

    assert portfolio_rows[0]["id"] == 'https://nzsuperfund.co.nz/custodian/fundPortfolio/ZN1114'
    assert portfolio_rows[0]["type"] == "https://spec.edmcouncil.org/fibo/ontology/SEC/Funds/CollectiveInvestmentVehicles/FundPortfolio"
    assert portfolio_rows[0]["label"] == "ZN1114"



