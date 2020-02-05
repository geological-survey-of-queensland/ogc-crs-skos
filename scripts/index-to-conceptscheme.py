import requests
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, SKOS, DCTERMS, XSD
from io import StringIO
import re


def get_identifiers():
    pattern = re.compile('<identifier>(.*)</identifier>')
    # # TESTING
    # with open('index.xml') as f:
    #     return re.findall(pattern, f.read())

    r = requests.get('http://www.opengis.net/def/crs/EPSG/0')
    if r.ok:
        return re.findall(pattern, StringIO(r.text).read())
    else:
        raise Exception('Response from http://www.opengis.net/def/crs/EPSG/0, was {}'.format(r.status_code))


def convert_to_graph(list_of_ids):
    g = Graph()
    g.bind('skos', SKOS)
    g.bind('dct', DCTERMS)
    cs_uri = URIRef('http://www.opengis.net/def/crs/EPSG/0/')
    g.add((
        cs_uri,
        RDF.type,
        SKOS.ConceptScheme
    ))
    g.add((
        cs_uri,
        SKOS.prefLabel,
        Literal('Coordinate Reference Systems')
    ))

    for id in list_of_ids:
        g.add((
            cs_uri,
            SKOS.hasTopConcept,
            URIRef(id)
        ))

    return g


if __name__ == '__main__':
    ids = get_identifiers()
    g = convert_to_graph(ids)
    print(g.serialize(format='turtle').decode('utf-8'))
