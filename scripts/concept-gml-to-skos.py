import requests
from lxml import etree
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, SKOS, DCTERMS, XSD
from io import StringIO


def get_xml_tree(epsg_uri):
    # # TESTING
    # return etree.parse(open('example.xml'))

    r = requests.get(epsg_uri)
    if r.ok:
        return etree.parse(StringIO(r.content.decode('utf-8').replace('<?xml version="1.0" encoding="UTF-8"?>', '')))
    else:
        raise Exception('Response from given URI, {}, was {}'.format(epsg_uri, r.status_code))


def extract_variables_from_lxml_tree(tree):
    vars = {}
    namespaces = tree.getroot().nsmap
    namespaces['epsg'] = 'urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset'
    namespaces['xlink'] = 'http://www.w3.org/1999/xlink'

    vars['source'] = tree.xpath('//epsg:informationSource/text()', namespaces=namespaces)[0]
    vars['modified'] = tree.xpath('//epsg:revisionDate/text()', namespaces=namespaces)[0]
    vars['historyNote'] = tree.xpath('//epsg:changeID/@xlink:href', namespaces=namespaces)
    if tree.xpath('//epsg:sourceGeographicCRS/@xlink:href', namespaces=namespaces)[0] == 'true':
        vars['status'] = 'deprecated'
    else:
        vars['status'] = 'stable'
    # vars['wasDerivedFrom'] = tree.xpath('//epsg:revisionDate/text()', namespaces=namespaces)[0]
    vars['notation'] = tree.xpath('//gml:identifier/text()', namespaces=namespaces)[0]
    vars['prefLabel'] = tree.xpath('//gml:name/text()', namespaces=namespaces)[0]
    vars['scopeNote'] = tree.xpath('//gml:scope/text()', namespaces=namespaces)[0]

    return vars


def convert_variables_to_graph(epsg_uri, vars):
    g = Graph()
    g.bind('skos', SKOS)
    g.bind('dct', DCTERMS)
    this_concept_uri = URIRef(epsg_uri)
    g.add((
        this_concept_uri,
        RDF.type,
        SKOS.Concept
    ))

    g.add((
        this_concept_uri,
        DCTERMS.source,
        Literal(vars['source'])
    ))

    history_note_text = Literal(
        'Edits to this entry have the following OGC Change Request IDs: {}'
            .format(', '.join(vars['historyNote'])), lang='en'
    )
    g.add((
        this_concept_uri,
        SKOS.historyNote,
        history_note_text
    ))

    g.bind('reg', 'http://purl.org/linked-data/registry#')
    g.bind('status', 'http://linked.data.gov.au/def/reg-status/')
    g.add((
        this_concept_uri,
        URIRef('http://purl.org/linked-data/registry#status'),
        URIRef('http://linked.data.gov.au/def/reg-status/{}'.format(vars['status'])),
    ))

    g.add((
        this_concept_uri,
        SKOS.notation,
        Literal(vars['notation'], datatype=XSD.token)
    ))

    g.add((
        this_concept_uri,
        SKOS.prefLabel,
        Literal(vars['prefLabel'])
    ))

    g.add((
        this_concept_uri,
        SKOS.scopeNote,
        Literal(vars['scopeNote'], lang='en')
    ))

    return g


if __name__ == '__main__':
    epsg_uri = 'http://www.opengis.net/def/crs/EPSG/0/4283'
    tree = get_xml_tree(epsg_uri)
    vars = extract_variables_from_lxml_tree(tree)
    g = convert_variables_to_graph(epsg_uri, vars)
    print(g.serialize(format='turtle').decode('utf-8'))
    # from pprint import pprint
    # pprint(vars)

