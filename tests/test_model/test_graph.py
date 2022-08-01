from sparkjobtest.util import session
from sparkjobtest.model import graph
# from tests.shared import graph

def setup_module():
    pass


def test_build_df_from_graph(create_testing_pyspark_session,
                             init_db):
    g = graph.read_graph(location="tests/fixtures/generated_graph.json")

    result = graph.build_cbor_df(g.value)

    assert result.is_right()

    df = result.value

    portfolio_rows = [d[0] for d in df.select(df.Portfolio).collect()]

    assert len(portfolio_rows) == 1
    
    row1 = portfolio_rows[0]

    assert row1["id"] == 'https://nzsuperfund.co.nz/custodian/fundPortfolio/ZN1114'
    assert row1["type"] == "https://spec.edmcouncil.org/fibo/ontology/SEC/Funds/CollectiveInvestmentVehicles/FundPortfolio"
    assert row1["label"] == "ZN1114"



