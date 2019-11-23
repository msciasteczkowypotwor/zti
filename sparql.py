from pynif import NIFCollection
collection = NIFCollection(uri='http://freme-project.eu')

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
print(generated_nif)