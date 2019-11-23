from rdflib import Graph
import pprint
import spacy
import en_core_web_sm

#g=Graph()
#g.parse("test.xml.ttl", format='ttl')

#g.serialize('test.rdf', format='pretty-xml', max_depth=3)

g = Graph()
g.load('test.xml.ttl', format='ttl')

spacy.nlp = en_core_web_sm.load()
for row in g.query('select ?s where { [] nif:isString ?s .}'):
# print(row.s)
    statement = row.s
    doc = spacy.nlp(str(statement))
    #print([(X.text, X.label_) for X in doc.ents])
    for X in doc.ents:
        start = statement.find(X.text)
        stop = start+len(X.text)
        print(X.text, X.start_char, X.end_char,)
