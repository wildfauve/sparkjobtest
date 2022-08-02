from sparkjobtest import job

from sparkjobtest.util import session
from tests.shared import graph

def setup_module():
    # graph.gen_test_graph()
    pass

def test_job_runs_successfully(create_testing_pyspark_session,
                               init_db,
                               mocker):
    mocker.patch("sparkjobtest.util.config.dbfs", None)
    mocker.patch("sparkjobtest.util.config.batch_source_folder", "tests/fixtures")

    result = job.job(args=sys_args())

    assert result.is_right()

    df = session.session().table('dataProduct_cbor.cbor')

    portfolio_ids =  [d[0] for d in df.select(df.Portfolio.id).collect()]

    assert portfolio_ids == ['https://nzsuperfund.co.nz/custodian/fundPortfolio/ZN1114']

    man = session.session().table('dataProduct_cbor.jobManifest')

    assert man.filter((man.uuid == result.value.uuid) & (man.processState == "complete")).collect()


def test_job_runs_updates_graph(create_testing_pyspark_session,
                                init_db,
                                mocker):

    mocker.patch("sparkjobtest.util.config.dbfs", None)
    mocker.patch("sparkjobtest.util.config.batch_source_folder", "tests/fixtures")


    #TODO: Refactor to apply a real update to the CBOR; same NAVDate and different NAVDate
    result1 = job.job(args=sys_args())

    assert result1.is_right()

    result2 = job.job(args=sys_args())

    assert result2.is_right()

    df = session.session().table('dataProduct_cbor.cbor')

    portfolios = set([d[0] for d in df.select(df.Portfolio.id).collect()])

    assert portfolios == set(['https://nzsuperfund.co.nz/custodian/fundPortfolio/ZN1114', 'https://nzsuperfund.co.nz/custodian/fundPortfolio/ZN1114'])


#
# Helpers
#
def sys_args():
    return [
            "--batches",
            "generated_graph.json"
          ]