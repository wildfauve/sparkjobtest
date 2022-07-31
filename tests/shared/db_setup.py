import pytest


@pytest.fixture
def init_db():
    from sparkjobtest.util import session
    session.session().sql("drop database IF EXISTS dataProduct_cbor CASCADE")
    session.session().sql("create database IF NOT EXISTS dataProduct_cbor")
