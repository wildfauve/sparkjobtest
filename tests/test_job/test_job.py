from sparkjobtest import job

from sparkjobtest.util import session
from tests.shared import graph

def setup_module():
    # graph.gen_test_graph()
    pass

def test_job_runs_successfully(create_testing_pyspark_session,
                               init_db):
    result = job.job(ids=None, location="tests/fixtures/generated_graph.json")

    assert result.is_right()

    df = session.session().table('dataProduct_cbor.graph')


    portfolio_ids =  [d[0] for d in df.select(df.Portfolio.id).collect()]

    assert portfolio_ids == ['https://nzsuperfund.co.nz/custodian/fundPortfolio/ZN1114']

    man = session.session().table('dataProduct_cbor.jobManifest')

    assert man.filter((man.uuid == result.value.uuid) & (man.processState == "complete")).collect()


def test_job_runs_updates_batch(create_testing_pyspark_session,
                                init_db):

    result1 = job.job(ids=None, location="tests/fixtures/test1.csv")

    assert result1.is_right()

    result2 = job.job(ids=None, location="tests/fixtures/test2.csv")

    assert result2.is_right()

    df = session.session().table('dataProduct_cbor.batch')

    names = set([d[0] for d in df.select(df.name).collect()])

    assert names == set(["Dinsdale", "Bronzino", "Claude", "Fyodoro"])


