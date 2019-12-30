import spacy
import en_core_web_lg  # sudo python -m spacy download en_core_web_lg
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON
import os

import re

FINDING_REF_CONTEXT = "^<.*>$"
FINDING_PART_REF_CONTEXT = ".*char="


def find(text, regex):
    return re.findall(regex, text, re.M)[0]

def create_note(anchor_of, begin_index, end_index, dbpedia, reference):
    part_context = find(reference, FINDING_PART_REF_CONTEXT)
    return part_context + begin_index + ',' + end_index + '>\n\t' \
          '   a                  nif:RFC5147String , nif:String ;  nif:anchorOf\n\t' \
          '   nif:anchorOf       "' + anchor_of +'"@en;\n\t' \
                                              '   if:beginIndex      "' + begin_index +'"^^xsd:nonNegativeInteger;\n\t' \
                                              '   nif:endIndex       "' + end_index +'"^^xsd:nonNegativeInteger;\n\t   ' \
                                              'nif:referenceContext ' + reference + ';\n\t' \
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
    if dbpedia_check(name):
        return "dbpedia:" + name
    return '<http://aksw.org/notInWiki/' + name + '>'






def find_named_entitys(file_name):
    g = Graph()
    g.load(file_name, format='ttl')
    f = open(file_name, 'r')
    output = f.read()
    print(output)
    full_context = find(output, FINDING_REF_CONTEXT)

    for row in g.query('select ?s where { [] nif:isString ?s .}'):
        statement = row.s
        doc = spacy.nlp(str(statement))
        for X in doc.ents:
            a = X.text.replace(" ", "_")

            if X.label_ == "PERSON" or X.label_ == "ORG" or X.label_ == "GPE":
                start = statement.find(X.text)
                stop = start + len(X.text)
                print(X.text, X.label_, X.start_char, X.end_char)
                output += "\n" + create_note(X.text, str(start), str(stop), create_context(a), full_context)
    return output


spacy.nlp = en_core_web_lg.load()
input_directory = 'inputs/'
for filename in os.listdir(input_directory):
    print(filename)
    f = open('outputs/'+filename,'w')
    f.write(find_named_entitys(input_directory+filename))


