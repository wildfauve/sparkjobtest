from rdflib import Namespace, Graph, Literal, RDF

sfo = Namespace('https://nzsuperfund.co.nz/ontology/')
lcc_lr = Namespace("https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/")

def gen_test_graph():
    g = Graph()

    bind(g)
    build(g)
    as_ld(g=g, context=ld_context(), file="tests/fixtures/graph.json")
    return g


def ld_context():
    return {"@vocab": "https://nzsuperfund.co.nz/ontology/",
            "@language": "en",
            "lcc-lr": "https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/"}


def bind(g):
    g.bind('', sfo)
    g.bind('sfo', sfo)
    g.bind('lcc-lr', lcc_lr)
    return g


def build(g):
    zn1111 = g.resource(sfo.term("custodianPortfolio/zn1111"))
    zn1111.add(RDF.type, sfo.FundPortfolio)
    zn1111.add(lcc_lr.hasTag, Literal("zn1114"))
    pass


def p(g, t="turtle", context=None, file=None):
    if t == "turtle":
        txt = g.serialize(format=t)
    else:
        txt = g.serialize(format="json-ld", context=context, indent=4)
    if file:
        with open(file, 'w') as f:
            f.write(txt)


def as_ld(g, context, file=None):
    p(g, t="json-ld", context=context, file=file)
