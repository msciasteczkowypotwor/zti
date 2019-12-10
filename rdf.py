from rdflib import Graph
import spacy
import en_core_web_sm     #sudo python -m spacy download en_core_web_sm
from pynif import NIFCollection

from SPARQLWrapper import SPARQLWrapper, JSON

def create_note(anchor_of,begin_index,end_index,leng,dbpedia):
    context ="<http://example.com/example-task1 char=0," + leng + ">"
    return '<http://example.com/example-task1#char=' + begin_index + ',' + end_index + '>\n\t' \
          '   a                  nif:RFC5147String , nif:String ;  nif:anchorOf\n\t' \
          '   nif:anchorOf       "' + anchor_of +'"@en;\n\t' \
                                              '   if:beginIndex      "' + begin_index +'"^^xsd:nonNegativeInteger;\n\t' \
                                              '   nif:endIndex       "' + end_index +'"^^xsd:nonNegativeInteger;\n\t   ' \
                                              'nif:referenceContext ' + context + ';\n\t' \
                                              '   itsrdf:taIdentRef  ' + dbpedia + '.\n'


def dbpedia_check(query):
    ontologies = ["Person", "Organisation", "Place"]
    for ont in ontologies:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
        ask
        where {<http://dbpedia.org/resource/""" + query + """> rdf:type <http://dbpedia.org/ontology/""" + ont + """>}
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if (results['boolean']):
            return True
    return False



def create_context(name):
    if(dbpedia_check(name)):
        return "dbpedia:"+name
    return '<http://aksw.org/notInWiki/'+name+'>'






#g=Graph()
#g.parse("test.xml.ttl", format='ttl')

#g.serialize('test.rdf', format='pretty-xml', max_depth=3)
collection = NIFCollection(uri='http://freme-project.eu')

g = Graph()
g.load('test.xml.ttl', format='ttl')

spacy.nlp = en_core_web_sm.load()


f = open('test.xml.ttl','r')
output = f.read()



for row in g.query('select ?s where { [] nif:isString ?s .}'):
# print(row.s)
    statement = row.s
    doc = spacy.nlp(str(statement))
    for X in doc.ents:
        a = X.text.replace(" ", "_")

        if X.label_=="PERSON" or X.label_=="ORG" or X.label_=="GPE":
            start = statement.find(X.text)
            stop = start + len(X.text)
            print(X.text, X.label_, X.start_char, X.end_char)
            output += create_note(X.text, str(start), str(stop), str(len(statement)), create_context(a))




print(output)
