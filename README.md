# OGC CRS to SKOS transform scripts
This repository contains Python scripts that can be used to transform the [Open Geospatial Consortium (OGC)](https://www.opengeospatial.org)'s published Coordinate Reference System (CRS) data from their original XML format into [Resource Description Framework (RDF)](http://www.w3.org/TR/rdf11-concepts/) data, according to the [Simple Knowledge Organization System (SKOS)](https://www.w3.org/TR/skos-reference/) model.


## EPSG CRS Instance / Concept Example
The OGC's published information for the *Geodetic Datum of Australia '94 (GDA94)* is available at the persistent URI <http://www.opengis.net/def/crs/EPSG/0/4283> which uses GDA94's EPSG code, 4283 as its identifier.

The information published is XML data according to the [Geographic Markup Language (GML)](https://www.opengeospatial.org/standards/gml) standard and some extended schemas just for EPSG codes and, for GDA94 looks like this:

```
<?xml version="1.0" encoding="UTF-8"?>
<gml:GeodeticCRS xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iogp-crs-4283">
  <gml:metaDataProperty>
    <epsg:CommonMetaData xmlns:epsg="urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset">
      <epsg:type>geographic 2D</epsg:type>
      <epsg:alias code="8484" codeSpace="urn:ogc:def:naming-system:EPSG::1046" alias="368" />
      <epsg:alias code="8485" codeSpace="urn:ogc:def:naming-system:EPSG::1047" alias="GDA94 - LatLon" />
      <epsg:informationSource>EPSG. See 3D CRS for original information source.</epsg:informationSource>
      <epsg:revisionDate>2019-09-17</epsg:revisionDate>
      <epsg:changes>
        <epsg:changeID xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="urn:ogc:def:change-request:EPSG::2003.370" />
        <epsg:changeID xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="urn:ogc:def:change-request:EPSG::2007.079" />
        <epsg:changeID xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="urn:ogc:def:change-request:EPSG::2011.004" />
        <epsg:changeID xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="urn:ogc:def:change-request:EPSG::2014.005" />
        <epsg:changeID xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="urn:ogc:def:change-request:EPSG::2019.033" />
      </epsg:changes>
      <epsg:show>true</epsg:show>
      <epsg:isDeprecated>false</epsg:isDeprecated>
    </epsg:CommonMetaData>
  </gml:metaDataProperty>
  <gml:metaDataProperty>
    <epsg:CRSMetaData xmlns:epsg="urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset">
      <epsg:projectionConversion xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="urn:ogc:def:coordinateOperation:EPSG::15593" />
      <epsg:sourceGeographicCRS xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="urn:ogc:def:crs:EPSG::4939" />
    </epsg:CRSMetaData>
  </gml:metaDataProperty>
  <gml:identifier codeSpace="IOGP">urn:ogc:def:crs:EPSG::4283</gml:identifier>
  <gml:name>GDA94</gml:name>
  <gml:domainOfValidity xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="urn:ogc:def:area:EPSG::4177" />
  <gml:scope>Horizontal component of 3D system.</gml:scope>
  <gml:ellipsoidalCS xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="urn:ogc:def:cs:EPSG::6422" />
  <gml:geodeticDatum xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="urn:ogc:def:datum:EPSG::6283" />
</gml:GeodeticCRS>
```

The script [concept-gml-to-skos.py](scripts/concept-gml-to-skos.py) can retrieve GML data and convert it to a RDF output according to the SKOS data model that, for GDA94, looks like this:

```
@prefix dct: <http://purl.org/dc/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix reg: <http://purl.org/linked-data/registry#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix status: <https://linked.data.gov.au/def/reg-status/> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://www.opengis.net/def/crs/EPSG/0/4283> a skos:Concept ;
    dct:source       "EPSG. See 3D CRS for original information source." ;
    reg:status       status:stable ;
    skos:historyNote "Edits to this entry have the following OGC Change Request IDs: urn:ogc:def:change-request:EPSG::2003.370, urn:ogc:def:change-request:EPSG::2007.079, urn:ogc:def:change-request:EPSG::2011.004, urn:ogc:def:change-request:EPSG::2014.005, urn:ogc:def:change-request:EPSG::2019.033"@en ;
    skos:notation    "urn:ogc:def:crs:EPSG::4283"^^xsd:token ;
    skos:prefLabel   "GDA94" ;
    skos:scopeNote   "Horizontal component of 3D system."@en .
```

The RDF information above is a small subset of the original information: only that which works within normal SKOS contexts. 


# EPSG listing / SKOS ConceptScheme
The simple listing of all EPSG URIs is given by the OGC system at <http://www.opengis.net/def/crs/EPSG/0> like this:

```
<?xml version="1.0" encoding="ISO-8859-1"?>
<identifiers at='http://www.opengis.net/def/crs/EPSG/0' xmlns='http://www.opengis.net/crs-nts/1.0' xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd">
 <identifier>http://www.opengis.net/def/crs/EPSG/0/2000</identifier>
 <identifier>http://www.opengis.net/def/crs/EPSG/0/20004</identifier>
 ...
 <identifier>http://www.opengis.net/def/crs/EPSG/0/9333</identifier>
 <identifier>http://www.opengis.net/def/crs/EPSG/0/9335</identifier>
</identifiers>
```

The script [index-to-conceptscheme.py](scripts/index-to-conceptscheme.py) reads that index and creates:

```
@prefix dct: <http://purl.org/dc/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://www.opengis.net/def/crs/EPSG/0/> a skos:ConceptScheme ;
    skos:hasTopConcept <http://www.opengis.net/def/crs/EPSG/0/2000>,
        <http://www.opengis.net/def/crs/EPSG/0/20004>,
        <http://www.opengis.net/def/crs/EPSG/0/20005>,
        ...
        <http://www.opengis.net/def/crs/EPSG/0/9333>,
        <http://www.opengis.net/def/crs/EPSG/0/9335> ;
    skos:prefLabel "Coordinate Reference Systems" .
```


## License
The content of this API is licensed for use under the [Creative Commons Zero License](https://creativecommons.org/choose/zero/). You are essentially free to use this code however you see fit.


## Contacts
*owner*:  
**Geological Survey of Queensland**  
*Within the Queensland Department of Natural Resources, Mines & Energy*  
1 William St, Brisbane, Queensland, Australia  
<https://www.business.qld.gov.au/industries/mining-energy-water/resources/geoscience-information/gsq>  
<GSQOpenData@dnrme.qld.gov.au>  

*author*:  
**Nicholas Car**  
[SURROUND Australia Pty Ltd](https://surroundaustralia.com)  
<nicholas.car@surroundaustralia.com>  
<http://orcid.org/0000-0002-8742-7730>  