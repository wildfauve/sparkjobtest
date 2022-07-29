from sparkjobtest import job

from sparkjobtest.util import session

def setup_module():
    pass

def test_job_returns_true(create_testing_pyspark_session,
                          init_db):
    result = job.job(ids=None, location="tests/fixtures/test.csv")

    df = session.session().table('dataProduct_cbor.batch')

    names = [d[0] for d in df.select(df.name).collect()]

    assert names == ["Dinsdale", "Bronzino"]
