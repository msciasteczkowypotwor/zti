from rdflib import Graph
import pprint

g=Graph()
g.parse("test.xml.ttl", format='ttl')

g.serialize('test.rdf', format='pretty-xml', max_depth=3)