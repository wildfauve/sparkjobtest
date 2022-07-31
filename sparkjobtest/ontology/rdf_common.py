import uuid
from rdflib import BNode, Literal
from rdflib.namespace import RDF

from . import rdf_prefix as P

# References (Jurisdictions)
aus = P.lcc_3166_1.AUS
usa = P.lcc_3166_1.USA
aud = P.fibo_fnd_acc_4217.AUD
usd = P.fibo_fnd_acc_4217.USD
nzd = P.fibo_fnd_acc_4217.NZD


def price(g, dealt, is_a, amt, has_observed_datetime=None, dt=None, base=None, price_term=P.sfo_cmn_ind_cur, as_blank=True, has_version=None):
    r = BNode() if as_blank else price_term.term("price/{}".format(str(uuid.uuid4())))
    g.add((r, RDF.type, is_a))
    if has_version:
        g.add((r, P.sfo.hasTemporalVersion, Literal(has_version)))
    if dt:
        g.add((r, P.fibo_fnd_dt_fd.hasObservedDateTime, dt))
    if has_observed_datetime:
        g.add((r, P.fibo_fnd_dt_fd.hasObservedDateTime, has_observed_datetime))
    g.add((r, P.fibo_fnd_acc_cur.hasAmount, amt))
    g.add((r, P.fibo_fnd_acc_cur.hasCurrency, dealt))
    return r

