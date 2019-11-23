from rdflib import Graph
import pprint
import spacy
import en_core_web_sm
from pynif import NIFCollection

#g=Graph()
#g.parse("test.xml.ttl", format='ttl')

#g.serialize('test.rdf', format='pretty-xml', max_depth=3)
collection = NIFCollection(uri='http://freme-project.eu')
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





context = collection.add_context(uri='http://freme-project.eu',
                                 mention='Diego Maradona is from Argentina.')
context.add_phrase(
    beginIndex=0,
    endIndex=14,
    taClassRef=['http://dbpedia.org/ontology/SportsManager', 'http://dbpedia.org/ontology/Person', 'http://nerd.eurecom.fr/ontology#Person'],
    score=0.9869992701528016,
    annotator='http://freme-project.eu/tools/freme-ner',
    taIdentRef='http://dbpedia.org/resource/Diego_Maradona',
    taMsClassRef='http://dbpedia.org/ontology/SoccerManager')

context.add_phrase(
    beginIndex=23,
    endIndex=32,
    taClassRef=['http://dbpedia.org/ontology/PopulatedPlace', 'http://nerd.eurecom.fr/ontology#Location',
    'http://dbpedia.org/ontology/Place'],
    score=0.9804963628413852,
    annotator='http://freme-project.eu/tools/freme-ner',
    taMsClassRef='http://dbpedia.org/resource/Argentina')

generated_nif = collection.dumps(format='turtle')
file = open('b1.ttl', 'w')
file.write(str(generated_nif))
file.close()
#print(generated_nif)