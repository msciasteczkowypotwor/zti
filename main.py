import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

ex = "Democrats have accused the President of abusing his power by withholding nearly $400 million in US military aid to Ukraine and the prospect of a visit " \
     "to the Oval Office by new President Volodymyr Zelensky in order to coerce the former Soviet state into investigating a potential 2020 foe Joe Biden. Such conduct " \
     "they say is a worthy of impeachment because it amounts to bribery, puts Trump's own political goals ahead of America's national interests and effectively invited a foreign power to interfere in a US election"


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


sent = preprocess(ex)
#print(sent)

pattern = 'NP: {<DT>?<JJ>*<NN>}'


cp = nltk.RegexpParser(pattern)
cs = cp.parse(sent)
#print(cs)


iob_tagged = tree2conlltags(cs)
#pprint(iob_tagged)

ne_tree = nltk.ne_chunk(pos_tag(word_tokenize(ex)))
for x in range(89):
    print(ne_tree[x], x)

print(ne_tree.type('PERSON'))
#print(ne_tree[21][0], ne_tree[21][1])


